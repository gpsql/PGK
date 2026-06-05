extends Node3D

@onready var score_label = $HUD/ScoreLabel
@onready var lives_label = $HUD/LivesLabel
@onready var hp_bar = $HUD/HPBar

func _ready() -> void:
	GameManager.score_changed.connect(func(score): score_label.text = "Wynik: %d" % score)
	GameManager.lives_changed.connect(func(lives): lives_label.text = "Życia: %d" % lives)
	GameManager.hp_changed.connect(func(hp): hp_bar.value = hp)
	
	GameManager.game_over.connect(func(): get_tree().change_scene_to_file("res://game_over.tscn"))
	GameManager.level_complete.connect(func(): get_tree().change_scene_to_file("res://level_complete.tscn"))
	
	score_label.text = "Wynik: %d" % GameManager.score
	lives_label.text = "Życia: %d" % GameManager.lives
	hp_bar.max_value = GameManager.player_max_hp
	hp_bar.value = GameManager.player_hp
	
	var bgm = AudioStreamPlayer.new()
	var stream = preload("res://assets/audio/bgm_main.wav")
	stream.loop_mode = AudioStreamWAV.LOOP_FORWARD
	bgm.stream = stream
	bgm.volume_db = -10.0
	bgm.autoplay = true
	add_child(bgm)
