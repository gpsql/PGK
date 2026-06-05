extends Node3D

## Boss z wielofazową maszyną stanów (FSM) — Lab 14.
## Sygnał died emitowany przy śmierci.
## Zewnętrzny kod (main.gd) podłącza died → GameManager.level_complete.emit(),
## dzięki czemu boss nie tworzy zależności do GameManagera.

signal died
signal hp_changed(current: int, maximum: int)

enum State { IDLE, ATTACK, RETREAT, DEATH }

# [REFAKTORYZACJA: magic-numbers] wszystkie wartości liczbowe jako nazwane stałe
const MAX_HP:           int   = 10
const PHASE2_HP_RATIO:  float = 0.5   # próg fazy 2 (50 % HP)
const IDLE_DURATION:    float = 2.0   # sekundy w stanie IDLE
const ATTACK_DURATION:  float = 4.0   # sekundy w stanie ATTACK
const RETREAT_DURATION: float = 1.5   # sekundy w stanie RETREAT
const SHOOT_INTERVAL:   float = 1.0   # odstęp między strzałami (s)
const SWAY_AMPLITUDE:   float = 3.0   # zakres bujania w X
const RETREAT_DISTANCE: float = 5.0   # ile jednostek cofa się w Z
const FLASH_DURATION:   float = 0.08  # czas błysku przy trafieniu (s)

@export var enemy_bullet_scene: PackedScene
@export var explosion_scene: PackedScene

@onready var _mesh:     MeshInstance3D   = $MeshInstance3D
@onready var _shape_p1: CollisionShape3D = $HitboxPhase1/CollisionShape3D
@onready var _shape_p2: CollisionShape3D = $HitboxPhase2/CollisionShape3D

var current_state: State = State.IDLE
var hp:            int   = MAX_HP

var _phase2_active: bool  = false
var _state_timer:   float = 0.0
var _shoot_timer:   float = 0.0
var _start_x:       float = 0.0
var _tween:         Tween = null


func _ready() -> void:
	_start_x = position.x
	hp = MAX_HP
	_shape_p2.disabled = true   # faza 2 nieaktywna na starcie
	_enter_state(State.IDLE)


func _process(delta: float) -> void:
	if current_state == State.DEATH:
		return
	_state_timer += delta
	_shoot_timer += delta
	_tick_state()


# ---------------------------------------------------------------------------
# Maszyna stanów
# ---------------------------------------------------------------------------

## Logika przejść — wywoływana co klatkę z _process().
func _tick_state() -> void:
	match current_state:
		State.IDLE:
			if _state_timer >= IDLE_DURATION:
				_enter_state(State.ATTACK)
		State.ATTACK:
			if _shoot_timer >= SHOOT_INTERVAL:
				_shoot_timer = 0.0
				_try_shoot()
			if _state_timer >= ATTACK_DURATION:
				_enter_state(State.RETREAT)
		State.RETREAT:
			if _state_timer >= RETREAT_DURATION:
				_enter_state(State.ATTACK)


## Punkt wejścia do stanu — wywoływany raz przy każdej zmianie.
func _enter_state(new_state: State) -> void:
	current_state = new_state
	_state_timer  = 0.0
	match new_state:
		State.IDLE:    _start_idle()
		State.ATTACK:  _start_attack()
		State.RETREAT: _start_retreat()
		State.DEATH:   _start_death()


func _start_idle() -> void:
	_kill_tween()
	_tween = create_tween().set_loops().set_trans(Tween.TRANS_SINE)
	_tween.tween_property(self, "position:x", _start_x + SWAY_AMPLITUDE * 0.5, 1.0)
	_tween.tween_property(self, "position:x", _start_x - SWAY_AMPLITUDE * 0.5, 1.0)


func _start_attack() -> void:
	_shoot_timer = 0.0
	_kill_tween()
	_tween = create_tween().set_loops()
	_tween.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	_tween.tween_property(self, "position:x", _start_x + SWAY_AMPLITUDE, ATTACK_DURATION * 0.25)
	_tween.tween_property(self, "position:x", _start_x - SWAY_AMPLITUDE, ATTACK_DURATION * 0.25)


func _start_retreat() -> void:
	_kill_tween()
	var z_back := position.z + RETREAT_DISTANCE
	_tween = create_tween().set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	_tween.tween_property(self, "position:z", z_back,     RETREAT_DURATION * 0.5)
	_tween.tween_property(self, "position:z", position.z, RETREAT_DURATION * 0.5)


func _start_death() -> void:
	_kill_tween()
	_spawn_explosion()
	died.emit()
	queue_free()


# ---------------------------------------------------------------------------
# Logika trafień
# ---------------------------------------------------------------------------

## Publiczne API — wywoływane przez sygnały hitboxów (podłączane w main.gd).
## Zabezpieczenie przed wielokrotnym wejściem w DEATH.
func take_hit(damage: int) -> void:
	if current_state == State.DEATH:
		return
	hp -= damage
	hp = maxi(hp, 0)
	hp_changed.emit(hp, MAX_HP)
	_flash_hit()

	if hp <= int(MAX_HP * PHASE2_HP_RATIO) and not _phase2_active:
		_activate_phase2()

	if hp <= 0:
		_enter_state(State.DEATH)


func _activate_phase2() -> void:
	_phase2_active     = true
	_shape_p1.disabled = true   # zamiana aktywnego hitboxa
	_shape_p2.disabled = false

	# wizualna zmiana przy przejściu do fazy 2
	var mat := StandardMaterial3D.new()
	mat.albedo_color               = Color(0.55, 0.0, 1.0, 1.0)
	mat.emission_enabled           = true
	mat.emission                   = Color(0.35, 0.0, 0.8, 1.0)
	mat.emission_energy_multiplier = 3.0
	_mesh.set_surface_override_material(0, mat)


func _flash_hit() -> void:
	if not is_instance_valid(_mesh):
		return
	var flash_mat := StandardMaterial3D.new()
	flash_mat.albedo_color               = Color.WHITE
	flash_mat.emission_enabled           = true
	flash_mat.emission                   = Color(1.0, 0.4, 0.0, 1.0)
	flash_mat.emission_energy_multiplier = 6.0
	_mesh.set_surface_override_material(0, flash_mat)

	await get_tree().create_timer(FLASH_DURATION).timeout
	if not is_instance_valid(self):
		return
	if current_state != State.DEATH and not _phase2_active:
		_mesh.set_surface_override_material(0, null)


# ---------------------------------------------------------------------------
# Pomocniki — spawning
# ---------------------------------------------------------------------------

func _try_shoot() -> void:
	var players := get_tree().get_nodes_in_group("player")
	if players.is_empty():
		return
	var player_node := players[0] as Node3D
	if player_node == null:
		return
	var dir: Vector3 = (player_node.global_position - global_position).normalized()
	_spawn_bullet(dir)


## Wydzielony helper spawnu pocisku — unikamy powielania logiki.
func _spawn_bullet(dir: Vector3) -> void:
	if enemy_bullet_scene == null:
		push_warning("Boss: enemy_bullet_scene nie ustawione!")
		return
	var bullet: Area3D = enemy_bullet_scene.instantiate()
	get_tree().root.add_child(bullet)
	bullet.global_position = global_position
	bullet.direction       = dir


func _spawn_explosion() -> void:
	if explosion_scene == null:
		push_warning("Boss: explosion_scene nie ustawione!")
		return
	var exp: Node3D = explosion_scene.instantiate()
	get_tree().root.add_child(exp)
	exp.global_position = global_position


func _kill_tween() -> void:
	if _tween != null and _tween.is_valid():
		_tween.kill()
	_tween = null
