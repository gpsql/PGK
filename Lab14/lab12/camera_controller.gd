extends Camera3D

@export var camera_target: Node3D
@export var lag_speed: float = 8.0

var shake_intensity: float = 0.0

func _ready() -> void:
	add_to_group("camera")

func _process(delta: float) -> void:
	if camera_target:
		global_position = global_position.lerp(camera_target.global_position, lag_speed * delta)
	
	if shake_intensity > 0:
		var random_offset = Vector3(randf_range(-1.0, 1.0), randf_range(-1.0, 1.0), randf_range(-1.0, 1.0)) * shake_intensity
		global_position += random_offset
		shake_intensity = lerpf(shake_intensity, 0.0, 10.0 * delta)
		if shake_intensity < 0.01:
			shake_intensity = 0.0

func add_shake(amount: float) -> void:
	shake_intensity += amount
