extends Area3D

## Pocisk uniwersalny — używany zarówno przez gracza, jak i przez wrogów.
## direction ustaw po instantiate(), zanim pocisk trafi do drzewa sceny.
## Warstwa i maska kolizji ustawiane w scenie (.tscn), nie tutaj.

@export var speed: float = 30.0
@export var lifetime: float = 3.5
@export var direction: Vector3 = Vector3.ZERO   # musi być ustawione przez spawner!

var _time: float = 0.0


func _process(delta: float) -> void:
	if direction == Vector3.ZERO:
		push_warning("Bullet: direction nie zostało ustawione — pocisk stoi w miejscu!")
		return

	global_position += direction * speed * delta
	_time += delta
	if _time >= lifetime:
		queue_free()
