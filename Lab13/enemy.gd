extends Node3D

## Wróg: ma HP, buja się przez Tween, strzela w gracza.
## Sygnał died(points) emitowany przy śmierci — podłącza go WaveSpawner.

signal died(points: int)

@export var hp: int            = 2
@export var speed: float       = 3.0
@export var score_value: int   = 100
@export var sway_amplitude: float = 2.0
@export var sway_period: float    = 2.0
@export var shoot_interval: float = 2.5
@export var enemy_bullet_scene: PackedScene

var _start_x: float = 0.0
var _shoot_timer: float = 0.0
var _dead: bool = false


func _ready() -> void:
	$Area3D.area_entered.connect(_on_hit)
	_start_x = position.x
	_start_sway()
	# losowe przesunięcie timera, żeby wrogowie nie strzelali równocześnie
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
	# reagujemy tylko na pociski gracza (Layer 3 = wartość 4)
	if not (area.collision_layer & 4):
		return
	hp -= 1
	# wizualny feedback — rozjaśnienie przy trafieniu
	var mat := StandardMaterial3D.new()
	mat.albedo_color = Color(1.0, 0.5, 0.0, 1.0)
	mat.emission_enabled = true
	mat.emission = Color(1.0, 0.3, 0.0, 1.0)
	mat.emission_energy_multiplier = 3.0
	$MeshInstance3D.set_surface_override_material(0, mat)

	if hp <= 0:
		_die()
	else:
		# po chwili wróć do normalnego koloru
		await get_tree().create_timer(0.08).timeout
		if not _dead:
			$MeshInstance3D.set_surface_override_material(0, null)


func _die() -> void:
	_dead = true
	print("Wróg zniszczony! +%d pkt" % score_value)
	GameManager.add_score(score_value)
	queue_free()


func _try_shoot() -> void:
	if enemy_bullet_scene == null:
		return
	var players := get_tree().get_nodes_in_group("player")
	if players.is_empty():
		return

	var player_pos: Vector3 = players[0].global_position
	var dir := (player_pos - global_position).normalized()

	var bullet: Area3D = enemy_bullet_scene.instantiate()
	get_tree().root.add_child(bullet)
	bullet.global_position = global_position
	bullet.direction = dir
