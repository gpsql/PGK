extends PathFollow3D

## Automatyczny postęp wzdłuż szyny.
## Należy do grupy "rail" — WaveSpawner pobiera globalną pozycję przez grupę.

@export var rail_speed: float = 0.05


func _ready() -> void:
	add_to_group("rail")


func _process(delta: float) -> void:
	progress_ratio += rail_speed * delta
	if progress_ratio >= 1.0:
		progress_ratio = 1.0
		set_process(false)
