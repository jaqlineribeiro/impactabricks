#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, TouchSensor
from pybricks.parameters import Port, Direction, Stop, Color, Button
from pybricks.tools import wait

class RobotController:
    def _init_(self):
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
        """Escaneia as 6 faces do cubo mágico usando RGB"""
        self.ev3.screen.clear()
        self.ev3.screen.print("Escaneando...")
        cores_detectadas = []

        for face in range(6):
            self.ev3.screen.print("Face " + str(face+1))
            face_cores = []
            
            for pos in range(9):  # 3x3 = 9 posições por face
                # Lê valores RGB
                r, g, b = self.color_sensor.rgb()
                
                # Identifica a cor usando os mesmos ranges
                if r < 10 and g < 10 and b < 10:
                    cor = "Preto"
                elif (59 <= r <= 62) and (15 <= g <= 19) and (6 <= b <= 10):
                    cor = "Laranja"
                elif (42 <= r <= 45) and (10 <= g <= 12) and (6 <= b <= 9):
                    cor = "Vermelho"
                elif cor == Color.BLUE:
                    cor = "Azul"
                elif cor == Color.GREEN:
                    cor = "Verde"
                elif cor == Color.YELLOW:
                    cor = "Amarelo"
                elif cor == Color.WHITE:
                    cor = "Branco"
                else:
                    cor = "?"
                
                # Mostra no display
                self.ev3.screen.clear()
                self.ev3.screen.print("Face " + str(face+1))
                self.ev3.screen.print("Pos " + str(pos+1))
                self.ev3.screen.print("R:" + str(r))
                self.ev3.screen.print("G:" + str(g) + " B:" + str(b))
                self.ev3.screen.print("Cor: " + cor)
                
                face_cores.append(cor)
                wait(500)
                
            cores_detectadas.append(face_cores)
            self.motor_giro.run_angle(300, 270, then=Stop.HOLD)
            wait(1000)

        self.ev3.screen.print("Scan completo!")
        return cores_detectadas

    def executar_movimento(self, mov):
        """Executa um movimento do cubo mágico"""
        if mov == "R":
            self.giro_automatico_horizontal()
            self.giro_automatico_vertical()
            self.giro_automatico_horizontal()
            self.giro_automatico_vertical()
            self.giro_automatico_vertical()
            self.giro_automatico_vertical()
            self.giro_automatico_horizontal()
            self.giro_automatico_horizontal()
            self.giro_automatico_horizontal()
        elif mov == "R'":
            self.giro_automatico_horizontal()
            self.giro_automatico_vertical()
            self.giro_automatico_horizontal()
            self.giro_automatico_horizontal()
            self.giro_automatico_horizontal()
            self.giro_automatico_vertical()
            self.giro_automatico_vertical()
            self.giro_automatico_vertical()
            self.giro_automatico_horizontal()
            self.giro_automatico_horizontal()
            self.giro_automatico_horizontal()
        elif mov == "U":
            self.giro_automatico_vertical()
            self.giro_automatico_vertical()
            self.giro_automatico_horizontal()
            self.giro_automatico_vertical()
            self.giro_automatico_vertical()
        elif mov == "U'":
            self.giro_automatico_vertical()
            self.giro_automatico_vertical()
            self.giro_automatico_horizontal()
            self.giro_automatico_horizontal()
            self.giro_automatico_horizontal()
            self.giro_automatico_vertical()
            self.giro_automatico_vertical()
        elif mov == "F":
            self.giro_automatico_vertical()
            self.giro_automatico_horizontal()
            self.giro_automatico_vertical()
            self.giro_automatico_vertical()
            self.giro_automatico_vertical()

        elif mov == "F'":
            self.giro_automatico_vertical()
            self.giro_automatico_horizontal()
            self.giro_automatico_horizontal()
            self.giro_automatico_horizontal()
            self.giro_automatico_vertical()
            self.giro_automatico_vertical()
            self.giro_automatico_vertical()
        
        elif mov == "D":
            self.giro_automatico_horizontal()
            self.giro_automatico_horizontal()
            self.giro_automatico_horizontal()
            self.giro_automatico_horizontal()

        elif mov == "D'":
            self.giro_automatico_horizontal()
            self.giro_automatico_horizontal()
            self.giro_automatico_horizontal()
            self.giro_automatico_horizontal()

        elif mov == "B":
            self.giro_automatico_vertical()
            self.giro_automatico_vertical()
            self.giro_automatico_vertical()
            self.giro_automatico_horizontal()
            self.giro_automatico_vertical()

        elif mov == "B'":
            self.giro_automatico_vertical()
            self.giro_automatico_vertical()
            self.giro_automatico_vertical()
            self.giro_automatico_horizontal()
            self.giro_automatico_horizontal()
            self.giro_automatico_horizontal()
            self.giro_automatico_vertical()

        elif mov == "L":
            self.giro_automatico_horizontal()
            self.giro_automatico_horizontal()
            self.giro_automatico_horizontal()
            self.giro_automatico_vertical()
            self.giro_automatico_horizontal()
            self.giro_automatico_vertical()
            self.giro_automatico_horizontal()


        elif mov == "L'":
            self.giro_automatico_horizontal()
            self.giro_automatico_horizontal()
            self.giro_automatico_horizontal()
            self.giro_automatico_vertical()
            self.giro_automatico_horizontal()
            self.giro_automatico_horizontal()
            self.giro_automatico_horizontal()
            self.giro_automatico_vertical()
            self.giro_automatico_horizontal()
        wait(500)

    def resolver_cubo(self):
        self.ev3.screen.clear()
        self.ev3.screen.print("Resolvendo...")
        estado_cubo = cores_detectadas
        url = "https://rubiksolverapi.com/solve"
        payload = {'state': estado_cubo}
        response = requests.post(url, data=payload)
        solution = response.json()
        for mov in solution:
            self.executar_movimento(mov)
        self.ev3.screen.print("Resolvido!")

    
    def monitorar_rgb(self):
        """Monitora valores RGB puros para calibração manual"""
        self.ev3.screen.clear()
        self.ev3.screen.print("Monitor RGB")
        self.ev3.screen.print("Centro = sair")
        self.ev3.screen.print("Cima = marcar")
        
        while True:
            if Button.CENTER in self.ev3.buttons.pressed():
                break
            
            # Obtém valores RGB e ângulo
            r, g, b = self.color_sensor.rgb()
            angulo = self.motor_sensor.angle()
            
            # Mostra no display
            self.ev3.screen.clear()
            self.ev3.screen.print("Ang: " + str(angulo))
            self.ev3.screen.print("R: " + str(r))
            self.ev3.screen.print("G: " + str(g))
            self.ev3.screen.print("B: " + str(b))
            
            # Se pressionar UP, marca os valores
            if Button.UP in self.ev3.buttons.pressed():
                self.ev3.screen.clear()
                self.ev3.screen.print("Valores RGB:")
                self.ev3.screen.print("R=" + str(r))
                self.ev3.screen.print("G=" + str(g))
                self.ev3.screen.print("B=" + str(b))
                wait(2000)  # Mantém na tela por 2 segundos
            
            wait(100)
        
        self.ev3.screen.clear()
        self.ev3.screen.print("Monitoramento")
        self.ev3.screen.print("finalizado")
        wait(1000)

def main():
    robot = RobotController()
    robot.reset_posicao()
    cores = robot.escanear_cubo()
    robot.resolver_cubo()
    robot.giro_automatico_horizontal()
    robot.giro_automatico_horizontal()
    robot.giro_automatico_horizontal()
    robot.giro_automatico_horizontal()
    robot.giro_automatico_horizontal()


if _name_ == "_main_":
    main()
