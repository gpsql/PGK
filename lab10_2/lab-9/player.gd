extends Node3D

## Sterowanie statkiem w płaszczyźnie XY (lokalne względem PathFollow3D).
## Statek automatycznie jedzie z szyną — tutaj obsługujemy tylko odchylenie.

@export var move_speed: float = 5.0

const LIMIT_X: float = 4.0
const LIMIT_Y: float = 3.0

# Przechylenie wizualne statku przy ruchu
const TILT_AMOUNT: float = 0.3


func _process(delta: float) -> void:
	var dir := Vector2.ZERO

	if Input.is_action_pressed("ui_left"):
		dir.x -= 1.0
	if Input.is_action_pressed("ui_right"):
		dir.x += 1.0
	if Input.is_action_pressed("ui_up"):
		dir.y += 1.0
	if Input.is_action_pressed("ui_down"):
		dir.y -= 1.0

	position.x += dir.x * move_speed * delta
	position.y += dir.y * move_speed * delta

	# Ogranicz strefę manewrowania
	position.x = clamp(position.x, -LIMIT_X, LIMIT_X)
	position.y = clamp(position.y, -LIMIT_Y, LIMIT_Y)

	# Lekkie wizualne przechylenie statku przy ruchu bocznym
	rotation.z = lerp(rotation.z, -dir.x * TILT_AMOUNT, 10.0 * delta)
	rotation.x = lerp(rotation.x, dir.y * TILT_AMOUNT * 0.5, 10.0 * delta)
