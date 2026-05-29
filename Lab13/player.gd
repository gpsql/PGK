extends Node3D

## Sterowanie statkiem + strzelanie.
## Należy do grupy "player" — wrogowie pobierają pozycję przez grupę.

@export var move_speed: float = 5.0
@export var bullet_scene: PackedScene

const LIMIT_X: float  = 4.0
const LIMIT_Y: float  = 3.0
const TILT_AMOUNT: float = 0.3
const SHOOT_COOLDOWN: float = 0.3

var _shoot_cooldown: float = 0.0

@onready var anim_player: AnimationPlayer = $AnimationPlayer
@onready var engine_mesh: MeshInstance3D = $Model/EngineMesh

var is_invincible: bool = false
var _barrel_roll_cooldown: float = 0.0
const BARREL_ROLL_COOLDOWN_TIME: float = 3.0

var _engine_mat: StandardMaterial3D

func _ready() -> void:
	add_to_group("player")
	var base_mat = engine_mesh.get_surface_override_material(0)
	if base_mat:
		_engine_mat = base_mat.duplicate() as StandardMaterial3D
		_engine_mat.albedo_color = Color.GREEN
		engine_mesh.set_surface_override_material(0, _engine_mat)


func _process(delta: float) -> void:
	_handle_movement(delta)
	_handle_shooting(delta)
	_handle_barrel_roll(delta)


func _handle_movement(delta: float) -> void:
	var dir := Vector2.ZERO

	if Input.is_action_pressed("ui_left"):  dir.x -= 1.0
	if Input.is_action_pressed("ui_right"): dir.x += 1.0
	if Input.is_action_pressed("ui_up"):    dir.y += 1.0
	if Input.is_action_pressed("ui_down"):  dir.y -= 1.0

	position.x += dir.x * move_speed * delta
	position.y += dir.y * move_speed * delta
	position.x = clamp(position.x, -LIMIT_X, LIMIT_X)
	position.y = clamp(position.y, -LIMIT_Y, LIMIT_Y)

	rotation.z = lerp(rotation.z, -dir.x * TILT_AMOUNT, 10.0 * delta)
	rotation.x = lerp(rotation.x, dir.y * TILT_AMOUNT * 0.5, 10.0 * delta)


func _handle_shooting(delta: float) -> void:
	_shoot_cooldown -= delta
	if Input.is_action_pressed("ui_accept") and _shoot_cooldown <= 0.0:
		_shoot_cooldown = SHOOT_COOLDOWN
		_spawn_bullet()


func _spawn_bullet() -> void:
	if bullet_scene == null:
		push_warning("Player: bullet_scene nie jest ustawione!")
		return

	var bullet: Area3D = bullet_scene.instantiate()
	get_tree().root.add_child(bullet)
	bullet.global_position = global_position
	bullet.direction = Vector3(0.0, 0.0, -1.0)   # <— wymagane po zmianie bullet.gd

func _handle_barrel_roll(delta: float) -> void:
	if _barrel_roll_cooldown > 0.0:
		_barrel_roll_cooldown -= delta
		if _barrel_roll_cooldown <= 0.0 and _engine_mat:
			_engine_mat.albedo_color = Color.GREEN
			
	if Input.is_action_just_pressed("ui_select") and _barrel_roll_cooldown <= 0.0 and not is_invincible:
		is_invincible = true
		_barrel_roll_cooldown = BARREL_ROLL_COOLDOWN_TIME
		if _engine_mat:
			_engine_mat.albedo_color = Color.GRAY
		anim_player.play("barrel_roll")
		await anim_player.animation_finished
		is_invincible = false

func take_damage(amount: int = 1) -> void:
	if is_invincible:
		return
	GameManager.player_hit(amount)
	get_tree().call_group("camera", "add_shake", 0.5)

func _on_hitbox_area_body_entered(body: Node3D) -> void:
	if body is StaticBody3D:
		take_damage(1)
