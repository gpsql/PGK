extends Area3D

## Pocisk gracza.
## Warstwa kolizji: Layer 3 (wartość 4), Maska: Layer 2 (wartość 2) — reaguje tylko na wrogów/cele.
## Porusza się do przodu (-Z w przestrzeni globalnej), usuwa się po upływie lifetime lub trafieniu.

@export var speed: float = 30.0
@export var lifetime: float = 3.0

var _time: float = 0.0


func _process(delta: float) -> void:
	# Pocisk leci w przestrzeni globalnej, niezależnie od szyny
	global_position.z -= speed * delta
	_time += delta
	if _time >= lifetime:
		queue_free()
