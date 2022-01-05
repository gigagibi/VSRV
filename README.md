# Курсовая работа по ВСРВ (МИРЭА)
Программный модуль системы умного дома для управления умными розетками
Содержит:
- Эмулятор физических розеток
- Программный модуль
## Стек разработки
- Python 3
- Tkinter
- Paho Eclipse MQTT
- MQTT broker (к примеру, mosquitto)
## Как запустить
1. Установить библиотеку paho-mqtt
```pip install paho-mqtt```
2. Установить и запустить локально MQTT брокер
3. Запустить эмулятор розеток
```python socket_emul.py```
4. Запустить программный эмулятор
```python socket_module.py```
# Term paper at the subject "Real-time Computing Systems"
Software module of IOT smart house system for controlling smart sockets. Uses MQTT
Consists of:
- Socket emulator software
- Software module
## Tech stack
- Python 3
- Tkinter
- Paho Eclipse MQTT
- MQTT broker (mosquitto for example)
## How to run
1. Install paho-mqtt package
```pip install paho-mqtt```
2. Install and run MQTT broker
3. Run sockets emulator
```python socket_emul.py```
4. Run software module
```python socket_module.py```
