extends Node3D

## Wróg: ma HP, buja się przez Tween, strzela w gracza, zostawia eksplozję przy śmierci.
## Sygnał died(points) emitowany przy śmierci — podłącza go WaveSpawner.

signal died(points: int)

@export var hp:             int   = 2
@export var speed:          float = 3.0
@export var score_value:    int   = 100
@export var sway_amplitude: float = 2.0
@export var sway_period:    float = 2.0
@export var shoot_interval: float = 2.5
@export var enemy_bullet_scene: PackedScene
@export var explosion_scene:    PackedScene   # opcjonalna eksplozja przy śmierci

# [REFAKTORYZACJA: magic-numbers] stałe zamiast magicznych liczb w kodzie
const FLASH_DURATION:       float = 0.08
const FLASH_EMISSION_MULT:  float = 3.0
const HIT_ALBEDO:           Color = Color(1.0, 0.5, 0.0, 1.0)
const HIT_EMISSION:         Color = Color(1.0, 0.3, 0.0, 1.0)
const PLAYER_BULLET_LAYER:  int   = 4    # warstwa pocisków gracza (bit 3)

var _start_x:     float = 0.0
var _shoot_timer: float = 0.0
var _dead:        bool  = false


func _ready() -> void:
	$Area3D.area_entered.connect(_on_hit)
	_start_x = position.x
	_start_sway()
	_shoot_timer = randf_range(0.0, shoot_interval)


func _start_sway() -> void:
	var tween := create_tween()
	tween.set_loops()
	tween.set_trans(Tween.TRANS_SINE)
	tween.set_ease(Tween.EASE_IN_OUT)
	tween.tween_property(self, "position:x", _start_x + sway_amplitude, sway_period * 0.5)
	tween.tween_property(self, "position:x", _start_x - sway_amplitude, sway_period * 0.5)


func _process(delta: float) -> void:
	if _dead:
		return
	_shoot_timer += delta
	if _shoot_timer >= shoot_interval:
		_shoot_timer = 0.0
		_try_shoot()


func _on_hit(area: Area3D) -> void:
	if _dead:
		return
	if not (area.collision_layer & PLAYER_BULLET_LAYER):
		return
	hp -= 1
	# [REFAKTORYZACJA: long-methods] wizualny feedback wydzielony do _flash_hit()
	_flash_hit()
	if hp <= 0:
		_die()


# [REFAKTORYZACJA: long-methods] wydzielony z _on_hit — odpowiada tylko za flash
func _flash_hit() -> void:
	var mat := StandardMaterial3D.new()
	mat.albedo_color               = HIT_ALBEDO
	mat.emission_enabled           = true
	mat.emission                   = HIT_EMISSION
	mat.emission_energy_multiplier = FLASH_EMISSION_MULT
	$MeshInstance3D.set_surface_override_material(0, mat)

	await get_tree().create_timer(FLASH_DURATION).timeout
	if not _dead and is_instance_valid(self):
		$MeshInstance3D.set_surface_override_material(0, null)


func _die() -> void:
	_dead = true
	_spawn_explosion()
	GameManager.add_score(score_value)
	queue_free()


func _try_shoot() -> void:
	if enemy_bullet_scene == null:
		return
	var players := get_tree().get_nodes_in_group("player")
	if players.is_empty():
		return
	var player_node := players[0] as Node3D
	if player_node == null:
		return
	var dir: Vector3 = (player_node.global_position - global_position).normalized()
	# [REFAKTORYZACJA: duplicate-code] helper spawnu — ta sama logika co w bossie
	_spawn_bullet(dir)


# [REFAKTORYZACJA: duplicate-code] pomocnik spawnu pocisku — wydzielony, nie powielony
func _spawn_bullet(dir: Vector3) -> void:
	var bullet: Area3D = enemy_bullet_scene.instantiate()
	get_tree().root.add_child(bullet)
	bullet.global_position = global_position
	bullet.direction       = dir


func _spawn_explosion() -> void:
	if explosion_scene == null:
		return
	var exp: Node3D = explosion_scene.instantiate()
	get_tree().root.add_child(exp)
	exp.global_position = global_position
