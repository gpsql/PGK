extends Node3D

## Główna scena gry — podłącza HUD do sygnałów GameManagera i bossa.
## Boss NIE wywołuje GameManagera sam — main.gd pośredniczy przez sygnał died.

@onready var score_label:   Label       = $HUD/ScoreLabel
@onready var lives_label:   Label       = $HUD/LivesLabel
@onready var hp_bar:        ProgressBar = $HUD/HPBar
@onready var boss_hp_bar:   ProgressBar = $HUD/BossHPBar
@onready var boss_hp_label: Label       = $HUD/BossHPLabel
@onready var lock_on:       Panel       = $HUD/LockOnIndicator
@onready var camera:        Camera3D    = $Camera3D

# Kolory paska HP bossa (zielony → żółty → czerwony)
const BOSS_COLOR_HIGH := Color(0.15, 0.85, 0.15, 1.0)
const BOSS_COLOR_MID  := Color(0.90, 0.80, 0.10, 1.0)
const BOSS_COLOR_LOW  := Color(0.90, 0.10, 0.10, 1.0)

# Progi zmiany koloru (ratio HP)
const COLOR_THRESHOLD_HIGH: float = 0.6
const COLOR_THRESHOLD_MID:  float = 0.3

var _boss: Node3D = null


func _ready() -> void:
	_connect_hud()
	_setup_boss()
	_play_bgm()


# ---------------------------------------------------------------------------
# HUD — GameManager
# ---------------------------------------------------------------------------

func _connect_hud() -> void:
	GameManager.score_changed.connect(func(s): score_label.text = "Wynik: %d" % s)
	GameManager.lives_changed.connect(func(l): lives_label.text = "Życia: %d" % l)
	GameManager.hp_changed.connect(func(h): hp_bar.value = h)

	GameManager.game_over.connect(
		func(): get_tree().change_scene_to_file("res://game_over.tscn"))
	GameManager.level_complete.connect(
		func(): get_tree().change_scene_to_file("res://level_complete.tscn"))

	score_label.text = "Wynik: %d" % GameManager.score
	lives_label.text = "Życia: %d" % GameManager.lives
	hp_bar.max_value = GameManager.player_max_hp
	hp_bar.value     = GameManager.player_hp


# ---------------------------------------------------------------------------
# Boss — podłączenie sygnałów i inicjalizacja paska HP
# ---------------------------------------------------------------------------

func _setup_boss() -> void:
	_boss = get_node_or_null("Boss")
	if _boss == null:
		boss_hp_bar.visible   = false
		boss_hp_label.visible = false
		lock_on.visible       = false
		return

	# Hitboxy podłączane tu, nie w bossie — boss nie wie nic o sobie samym z zewnątrz
	_boss.get_node("HitboxPhase1").area_entered.connect(func(_a): _boss.take_hit(1))
	_boss.get_node("HitboxPhase2").area_entered.connect(func(_a): _boss.take_hit(2))

	# Sygnał died → level_complete przez main, NIE bezpośrednio z bossa
	_boss.died.connect(_on_boss_died)
	_boss.hp_changed.connect(_on_boss_hp_changed)

	boss_hp_bar.max_value = _boss.MAX_HP
	boss_hp_bar.value     = _boss.MAX_HP
	boss_hp_bar.visible   = true
	boss_hp_label.visible = true
	_set_boss_bar_color(_boss.MAX_HP, _boss.MAX_HP)


func _on_boss_died() -> void:
	boss_hp_bar.visible   = false
	boss_hp_label.visible = false
	lock_on.visible       = false
	_boss = null
	GameManager.level_complete.emit()


func _on_boss_hp_changed(current: int, maximum: int) -> void:
	boss_hp_bar.value = current
	_set_boss_bar_color(current, maximum)


func _set_boss_bar_color(current: int, maximum: int) -> void:
	var ratio := float(current) / float(maximum)
	if ratio > COLOR_THRESHOLD_HIGH:
		boss_hp_bar.modulate = BOSS_COLOR_HIGH
	elif ratio > COLOR_THRESHOLD_MID:
		boss_hp_bar.modulate = BOSS_COLOR_MID
	else:
		boss_hp_bar.modulate = BOSS_COLOR_LOW


# ---------------------------------------------------------------------------
# Lock-on indicator (Zadanie *) — śledzi bossa na ekranie
# ---------------------------------------------------------------------------

func _process(_delta: float) -> void:
	_update_lock_on()


func _update_lock_on() -> void:
	if not is_instance_valid(_boss) or not is_instance_valid(camera):
		lock_on.visible = false
		return
	if camera.is_position_behind(_boss.global_position):
		lock_on.visible = false
		return
	var screen_pos := camera.unproject_position(_boss.global_position)
	lock_on.visible  = true
	lock_on.position = screen_pos - lock_on.size * 0.5


# ---------------------------------------------------------------------------
# Audio — muzyka tła
# ---------------------------------------------------------------------------

func _play_bgm() -> void:
	var bgm    := AudioStreamPlayer.new()
	var stream := preload("res://assets/audio/bgm_main.wav")
	stream.loop_mode = AudioStreamWAV.LOOP_FORWARD
	bgm.stream    = stream
	bgm.volume_db = -10.0
	bgm.autoplay  = true
	add_child(bgm)
