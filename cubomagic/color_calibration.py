# Este programa permite calibrar o sensor de cor para reconhecer as 6 cores do cubo
# e depois testar a identificação de cores em tempo real.

import time  # Para criar pausas entre operações
import json  # Para salvar/carregar dados de calibração em formato JSON
import os    # Para verificar existência de arquivos
from sensors import Color_sensor  # Nossa classe para o sensor de cor
from motors import Motor          # Nossa classe para controlar motores

class ColorCalibrator:
    """Classe para calibrar e identificar cores do cubo de Rubik"""
    
    def __init__(self):
        """Inicializa o calibrador de cores"""
        print("Inicializando calibrador de cores...")
        
        # Inicializar sensor de cor no Porto 2
        self.color_sensor = Color_sensor(2)
        
        # Inicializar motor para posicionar o sensor no Porto C
        self.motor_sensor = Motor(Motor.PORT_C)
        
        # Dicionário com as 6 cores padrão do cubo de Rubik
        # Cada cor tem um nome em português e um valor RGB (inicialmente None)
        self.cube_colors = {
            'white': {'name': 'Branco', 'rgb': None},
            'yellow': {'name': 'Amarelo', 'rgb': None},
            'red': {'name': 'Vermelho', 'rgb': None},
            'orange': {'name': 'Laranja', 'rgb': None},
            'blue': {'name': 'Azul', 'rgb': None},
            'green': {'name': 'Verde', 'rgb': None}
        }
        
        # Caminho para o arquivo onde serão salvos os dados de calibração
        self.calibration_file = "/home/robot/cubomagic/color_calibration.json"
        
        # Tenta carregar dados de calibração existentes
        self.load_calibration()
    
    def load_calibration(self):
        """Carrega dados de calibração salvos anteriormente"""
        # Verifica se o arquivo de calibração existe
        if os.path.exists(self.calibration_file):
            try:
                # Abre o arquivo e carrega os dados JSON
                with open(self.calibration_file, 'r') as f:
                    saved_colors = json.load(f)
                    # Atualiza o dicionário com os valores RGB salvos
                    for color_key, color_data in saved_colors.items():
                        if color_key in self.cube_colors:
                            self.cube_colors[color_key]['rgb'] = color_data['rgb']
                print("Calibração carregada com sucesso!")
            except Exception as e:
                # Trata erros durante o carregamento
                print("Erro ao carregar calibração: {}".format(e))
    
    def save_calibration(self):
        """Salva dados de calibração em arquivo JSON"""
        try:
            # Abre o arquivo para escrita e salva o dicionário em formato JSON
            with open(self.calibration_file, 'w') as f:
                json.dump(self.cube_colors, f)
            print("Calibração salva com sucesso!")
        except Exception as e:
            # Trata erros durante o salvamento
            print("Erro ao salvar calibração: {}".format(e))
    
    def calibrate_colors(self):
        """Calibra o sensor para reconhecer as cores do cubo"""
        print("\n=== CALIBRAÇÃO DE CORES ===")
        print("Posicione cada cor na frente do sensor quando solicitado.")
        
        # Posiciona o sensor para a calibração
        # Gira o motor 90 graus para colocar o sensor em posição
        self.motor_sensor.rotate(90)
        # Aguarda 1 segundo para estabilizar
        time.sleep(1)
        
        # Itera por cada cor no dicionário para calibrar
        for color_key, color_data in self.cube_colors.items():
            # Solicita ao usuário que posicione a cor específica
            input("Posicione a cor {} na frente do sensor e pressione Enter...".format(color_data['name']))
            
            # Faz 5 leituras para maior precisão
            readings = []
            for _ in range(5):
                # Obtém valores RGB do sensor
                rgb = self.color_sensor.get_rgb()
                readings.append(rgb)
                print("Leitura RGB: {}".format(rgb))
                # Aguarda meio segundo entre leituras
                time.sleep(0.5)
            
            # Calcula a média das 5 leituras para cada componente RGB
            # Usa divisão inteira (//) para obter valores inteiros
            avg_r = sum(r for r, g, b in readings) // len(readings)
            avg_g = sum(g for r, g, b in readings) // len(readings)
            avg_b = sum(b for r, g, b in readings) // len(readings)
            
            # Salva os valores RGB médios para esta cor
            self.cube_colors[color_key]['rgb'] = (avg_r, avg_g, avg_b)
            print("Cor {} calibrada: RGB = {}".format(color_data['name'], self.cube_colors[color_key]['rgb']))
        
        # Retorna o sensor à posição original
        self.motor_sensor.rotate(-90)
        
        # Salva os dados de calibração no arquivo
        self.save_calibration()
        print("Calibração de todas as cores concluída!")
    
    def identify_color(self, rgb):
        """
        Identifica a cor mais próxima com base nos valores RGB
        
        Args:
            rgb (tuple): Valores RGB (r, g, b) a serem identificados
        
        Returns:
            str: Chave da cor identificada (ex: 'white', 'red', etc.)
        """
        # Verifica se todas as cores foram calibradas
        if not all(color_data['rgb'] for color_data in self.cube_colors.values()):
            print("ERRO: Calibração incompleta. Execute a calibração primeiro.")
            return None
        
        # Inicializa variáveis para encontrar a cor mais próxima
        min_distance = float('inf')  # Distância mínima (inicialmente infinito)
        closest_color = None         # Cor mais próxima (inicialmente nenhuma)
        
        # Compara com cada cor calibrada
        for color_key, color_data in self.cube_colors.items():
            # Extrai componentes RGB da leitura atual
            r1, g1, b1 = rgb
            # Extrai componentes RGB da cor calibrada
            r2, g2, b2 = color_data['rgb']
            
            # Calcula a distância euclidiana no espaço RGB
            # Quanto menor a distância, mais próxima a cor
            distance = ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5
            
            # Se esta distância for menor que a mínima encontrada até agora
            if distance < min_distance:
                # Atualiza a distância mínima
                min_distance = distance
                # Atualiza a cor mais próxima
                closest_color = color_key
        
        # Retorna a chave da cor mais próxima
        return closest_color
    
    def test_identification(self):
        """Testa a identificação de cores em tempo real"""
        print("\n=== TESTE DE IDENTIFICAÇÃO DE CORES ===")
        print("Posicione diferentes cores na frente do sensor.")
        print("Pressione Ctrl+C para encerrar o teste.")
        
        # Posiciona o sensor para o teste
        self.motor_sensor.rotate(90)
        time.sleep(1)
        
        try:
            # Loop infinito para testar cores continuamente
            while True:
                # Obtém valores RGB do sensor
                rgb = self.color_sensor.get_rgb()
                # Identifica a cor mais próxima
                color = self.identify_color(rgb)
                
                # Exibe o resultado
                if color:
                    print("RGB: {} -> Cor identificada: {}".format(rgb, self.cube_colors[color]['name']))
                else:
                    print("RGB: {} -> Cor não identificada".format(rgb))
                
                # Aguarda 1 segundo antes da próxima leitura
                time.sleep(1)
        except KeyboardInterrupt:
            # Captura Ctrl+C para encerrar o loop
            print("\nTeste de identificação encerrado.")
        
        # Retorna o sensor à posição original
        self.motor_sensor.rotate(-90)

def main():
    """Função principal que exibe o menu e gerencia o programa"""
    # Cria uma instância do calibrador de cores
    calibrator = ColorCalibrator()
    
    # Loop principal do programa
    while True:
        # Exibe o menu de opções
        print("\n=== MENU DE CALIBRAÇÃO DE CORES ===")
        print("1. Calibrar cores")
        print("2. Testar identificação de cores")
        print("3. Sair")
        
        # Solicita a escolha do usuário
        choice = input("Escolha uma opção: ")
        
        # Executa a ação correspondente à escolha
        if choice == "1":
            calibrator.calibrate_colors()
        elif choice == "2":
            calibrator.test_identification()
        elif choice == "3":
            print("Encerrando programa...")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Ponto de entrada do programa
if __name__ == "__main__":
    main() 