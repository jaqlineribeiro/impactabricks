#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, TouchSensor
from pybricks.parameters import Port, Direction, Stop, Color, Button
from pybricks.tools import wait

class RobotController:
    def __init__(self):
        self.ev3 = EV3Brick()
        self.ev3.screen.clear()

        # Inicialização dos motores e sensores com verificação
        try:
            self.ev3.screen.print("Testando Motor A")
            self.motor_vertical = Motor(Port.A)
            self.ev3.screen.print("Motor A OK")
            wait(1000)
        except:
            self.ev3.screen.print("Erro Motor A")
            return

        try:
            self.ev3.screen.print("Testando Motor B")
            self.motor_giro = Motor(Port.B)
            self.ev3.screen.print("Motor B OK")
        except:
            self.ev3.screen.print("Erro Motor B")
        wait(1000)

        try:
            self.ev3.screen.print("Testando Motor C")
            self.motor_sensor = Motor(Port.C, Direction.COUNTERCLOCKWISE)
            self.ev3.screen.print("Motor C OK")
        except:
            self.ev3.screen.print("Erro Motor C")
        wait(1000)

        try:
            self.ev3.screen.print("Testando Cor S2")
            self.color_sensor = ColorSensor(Port.S2)
            self.ev3.screen.print("Sensor Cor OK")
        except:
            self.ev3.screen.print("Erro Sensor Cor")
        wait(1000)

        try:
            self.ev3.screen.print("Testando Toque S1")
            self.touch_sensor = TouchSensor(Port.S1)
            self.ev3.screen.print("Sensor Toque OK")
        except:
            self.ev3.screen.print("Erro Sensor Toque")
        wait(1000)

    def reset_posicao(self):
        """Reset para posição zero"""
        self.ev3.screen.clear()
        self.ev3.screen.print("Resetando...")
        self.motor_vertical.reset_angle(0)
        self.motor_giro.reset_angle(0)
        self.motor_sensor.reset_angle(0)
        self.motor_vertical.hold()
        self.motor_giro.hold()
        self.motor_sensor.hold()
        self.ev3.screen.print("Posicao Zero OK")
        wait(1000)

    def giro_automatico_vertical(self):
        self.ev3.screen.clear()
        self.ev3.screen.print("Girando 90...")
        for i in range(4):
            self.ev3.screen.clear()
            self.ev3.screen.print("Giro " + str(i+1))
            self.motor_vertical.run_angle(160, 90, then=Stop.HOLD)
            angulo = self.motor_vertical.angle()
            # Melhor feedback do ângulo
            self.ev3.screen.print("Giro: " + str(i+1))
            self.ev3.screen.print("Angulo atual:")
            self.ev3.screen.print(str(angulo) + " graus")
            wait(2000)  # Tempo maior para ler
        self.ev3.screen.print("Completo!")

    def giro_automatico_horizontal(self):
        self.ev3.screen.clear()
        self.ev3.screen.print("Girando 90 H...")
        for i in range(4):
            self.ev3.screen.clear()
            self.ev3.screen.print("Giro H " + str(i+1))
            self.motor_giro.run_angle(300, 270, then=Stop.HOLD)
            angulo = self.motor_giro.angle()
            # Melhor feedback do ângulo
            self.ev3.screen.print("Giro: " + str(i+1))
            self.ev3.screen.print("Angulo atual:")
            self.ev3.screen.print(str(angulo) + " graus")
            wait(2000)  # Tempo maior para ler
        self.ev3.screen.print("Completo H!")

    def giro_automatico_sensor(self):
        self.ev3.screen.clear()
        self.ev3.screen.print("Girando Sensor...")
        for i in range(1):
            self.ev3.screen.clear()
            self.ev3.screen.print("Giro S " + str(i+1))
            
            # Primeiro movimento
            self.motor_sensor.run_angle(100, -500, then=Stop.HOLD)
            angulo1 = self.motor_sensor.angle()
            self.ev3.screen.print("Pos inicial:")
            self.ev3.screen.print(str(angulo1) + " graus")
            wait(2000)
            
            wait(5000)
            
            # Segundo movimento
            self.motor_sensor.run_angle(100, 400, then=Stop.HOLD)
            angulo2 = self.motor_sensor.angle()
            self.ev3.screen.print("Pos final:")
            self.ev3.screen.print(str(angulo2) + " graus")
            wait(2000)
        
        self.ev3.screen.print("Completo S!")

    def escanear_cubo(self):
        """Escaneia as 6 faces do cubo mágico"""
        self.ev3.screen.clear()
        self.ev3.screen.print("Escaneando...")
        cores_detectadas = []

        for face in range(6):
            self.ev3.screen.print("Face " + str(face+1))
            face_cores = []
            for pos in range(9):  # 3x3 = 9 posições por face
                cor = self.color_sensor.color()
                face_cores.append(cor)
                self.ev3.screen.print(str(cor))
                wait(500)
                # Mover para próxima posição do cubo
                # self.motor_sensor.run_angle(100, 30)
            cores_detectadas.append(face_cores)
            self.motor_giro.run_angle(300, 270, then=Stop.HOLD)
            wait(1000)

        self.ev3.screen.print("Scan completo!")
        return cores_detectadas

    def executar_movimento(self, mov):
        """Executa um movimento do cubo mágico"""
        if mov == "R":
            self.motor_vertical.run_angle(160, 90, then=Stop.HOLD)
        elif mov == "R'":
            self.motor_vertical.run_angle(160, -90, then=Stop.HOLD)
        elif mov == "U":
            self.motor_giro.run_angle(300, 90, then=Stop.HOLD)
        elif mov == "U'":
            self.motor_giro.run_angle(300, -90, then=Stop.HOLD)
        elif mov == "F":
            self.motor_sensor.run_angle(100, 90, then=Stop.HOLD)
        elif mov == "F'":
            self.motor_sensor.run_angle(100, -90, then=Stop.HOLD)
        wait(500)

    def resolver_cubo(self):
        """Executa uma sequência fixa como exemplo de resolução"""
        self.ev3.screen.clear()
        self.ev3.screen.print("Resolvendo...")
        movimentos = ["R", "U", "R'", "U'", "F", "F"]
        for mov in movimentos:
            self.executar_movimento(mov)
        self.ev3.screen.print("Resolvido!")

def main():
    robot = RobotController()
    #robot.reset_posicao()
    # robot.giro_automatico_vertical()
    # robot.giro_automatico_horizontal()
    robot.giro_automatico_sensor()
    
    # Para teste: escanear cubo
    # cores = robot.escanear_cubo()
    # print(cores)  # Para usar via Bluetooth/USB depois

    # Resolver usando sequência mock
    #robot.resolver_cubo()

if __name__ == "__main__":
    main()
