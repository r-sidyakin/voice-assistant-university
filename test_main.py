from unittest import TestCase

from commands import Command, predict_command_by_name, VoiceRecognizer, load_commands


class UnitTest(TestCase):
    def test_positive_recognize_command(self):
        recognizer = VoiceRecognizer()
        data = recognizer.recognize_voice()
        self.assertEqual(recognizer.recognize_voice(), "тест")

    def test_negative_recognize_command(self):
        recognizer = VoiceRecognizer()
        self.assertNotEqual(recognizer.recognize_voice(), "не тест")

    def test_positive_variability_command(self):
        need_cmd = Command("открой браузер")
        not_need_cmd = Command("запусти калькулятор")
        self.assertEqual(predict_command_by_name("открывай браузер", [need_cmd, not_need_cmd]), need_cmd)

    def test_negative_variability_command(self):
        need_cmd = Command("открой браузер")
        not_need_cmd = Command("запусти калькулятор")
        self.assertEqual(predict_command_by_name("сделай что-то", [need_cmd, not_need_cmd]), None)

    def test_positive_loader_of_command(self):
        commands = load_commands("commands.json")
        self.assertNotEqual(commands, None)

    def test_negative_loader_of_command(self):
        commands = load_commands("wrong_path")
        self.assertEqual(commands, None)
