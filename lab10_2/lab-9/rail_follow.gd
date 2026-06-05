extends PathFollow3D

## Automatyczny postęp wzdłuż szyny (PathFollow3D).
## rail_speed: jaki ułamek całej ścieżki przejeżdżamy na sekundę.
## Przy rail_speed = 0.04 przejście trwa ~25 s; przy 0.07 trwa ~14 s.

@export var rail_speed: float = 0.05


func _process(delta: float) -> void:
	progress_ratio += rail_speed * delta

	# Po osiągnięciu końca szyny zatrzymaj się
	if progress_ratio >= 1.0:
		progress_ratio = 1.0
		set_process(false)
