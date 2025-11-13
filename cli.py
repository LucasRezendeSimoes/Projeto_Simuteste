#!/usr/bin/env python
"""CLI interativa para o Sistema de Agendamento."""
import requests
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import os
import sys

# Configuração
API_BASE_URL = "http://localhost:8001/api"
TIMEOUT = 5

class Colors:
    """Cores para terminal."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clear_screen():
    """Limpa a tela do terminal."""
    os.system('clear' if os.name == 'posix' else 'cls')

def print_header(text: str):
    """Imprime um cabeçalho."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}")
    print(f"{text:^60}")
    print(f"{'='*60}{Colors.ENDC}\n")

def print_success(text: str):
    """Imprime mensagem de sucesso."""
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")

def print_error(text: str):
    """Imprime mensagem de erro."""
    print(f"{Colors.RED}✗ {text}{Colors.ENDC}")

def print_info(text: str):
    """Imprime mensagem informativa."""
    print(f"{Colors.BLUE}ℹ {text}{Colors.ENDC}")

def print_warning(text: str):
    """Imprime mensagem de aviso."""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.ENDC}")

def menu_principal():
    """Menu principal."""
    clear_screen()
    print_header("SISTEMA DE AGENDAMENTO")
    print(f"{Colors.BOLD}O que deseja fazer?{Colors.ENDC}\n")
    print("  1. Gerenciar Usuários")
    print("  2. Gerenciar Agendamentos")
    print("  3. Visualizar Relatórios")
    print("  4. Sair\n")
    
    choice = input(f"{Colors.BOLD}Escolha uma opção (1-4): {Colors.ENDC}").strip()
    return choice

def menu_usuarios():
    """Menu de gerenciamento de usuários."""
    while True:
        clear_screen()
        print_header("GERENCIAMENTO DE USUÁRIOS")
        print(f"{Colors.BOLD}O que deseja fazer?{Colors.ENDC}\n")
        print("  1. Criar novo usuário")
        print("  2. Consultar usuário")
        print("  3. Deletar usuário")
        print("  4. Voltar ao menu principal\n")
        
        choice = input(f"{Colors.BOLD}Escolha uma opção (1-4): {Colors.ENDC}").strip()
        
        if choice == "1":
            criar_usuario()
        elif choice == "2":
            consultar_usuario()
        elif choice == "3":
            deletar_usuario()
        elif choice == "4":
            break
        else:
            print_error("Opção inválida!")
            input("Pressione ENTER para continuar...")

def criar_usuario():
    """Cria um novo usuário."""
    clear_screen()
    print_header("CRIAR NOVO USUÁRIO")
    
    try:
        name = input(f"{Colors.BOLD}Nome do usuário: {Colors.ENDC}").strip()
        if not name:
            print_error("Nome não pode ser vazio!")
            input("Pressione ENTER para continuar...")
            return
        
        email = input(f"{Colors.BOLD}Email do usuário: {Colors.ENDC}").strip()
        if not email or "@" not in email:
            print_error("Email inválido!")
            input("Pressione ENTER para continuar...")
            return
        
        payload = {"name": name, "email": email}
        response = requests.post(f"{API_BASE_URL}/users", json=payload, timeout=TIMEOUT)
        
        if response.status_code == 200:
            user = response.json()
            print_success(f"Usuário criado com sucesso!")
            print(f"\n{Colors.BOLD}ID:{Colors.ENDC} {user['id']}")
            print(f"{Colors.BOLD}Nome:{Colors.ENDC} {user['name']}")
            print(f"{Colors.BOLD}Email:{Colors.ENDC} {user['email']}")
            print(f"{Colors.BOLD}Ativo:{Colors.ENDC} {'Sim' if user['is_active'] else 'Não'}")
        else:
            print_error(f"Erro ao criar usuário: {response.json().get('detail', response.text)}")
    
    except requests.exceptions.ConnectionError:
        print_error("Não foi possível conectar à API. Verifique se o servidor está rodando.")
    except Exception as e:
        print_error(f"Erro: {str(e)}")
    
    input("\nPressione ENTER para continuar...")

def consultar_usuario():
    """Consulta um usuário existente."""
    clear_screen()
    print_header("CONSULTAR USUÁRIO")
    
    try:
        user_id = input(f"{Colors.BOLD}ID do usuário: {Colors.ENDC}").strip()
        
        if not user_id.isdigit():
            print_error("ID deve ser um número!")
            input("Pressione ENTER para continuar...")
            return
        
        response = requests.get(f"{API_BASE_URL}/users/{user_id}", timeout=TIMEOUT)
        
        if response.status_code == 200:
            user = response.json()
            print_success("Usuário encontrado!")
            print(f"\n{Colors.BOLD}ID:{Colors.ENDC} {user['id']}")
            print(f"{Colors.BOLD}Nome:{Colors.ENDC} {user['name']}")
            print(f"{Colors.BOLD}Email:{Colors.ENDC} {user['email']}")
            print(f"{Colors.BOLD}Ativo:{Colors.ENDC} {'Sim' if user['is_active'] else 'Não'}")
        elif response.status_code == 404:
            print_error("Usuário não encontrado!")
        else:
            print_error(f"Erro: {response.json().get('detail', response.text)}")
    
    except requests.exceptions.ConnectionError:
        print_error("Não foi possível conectar à API. Verifique se o servidor está rodando.")
    except Exception as e:
        print_error(f"Erro: {str(e)}")
    
    input("\nPressione ENTER para continuar...")

def deletar_usuario():
    """Deleta um usuário."""
    clear_screen()
    print_header("DELETAR USUÁRIO")
    
    try:
        user_id = input(f"{Colors.BOLD}ID do usuário a deletar: {Colors.ENDC}").strip()
        
        if not user_id.isdigit():
            print_error("ID deve ser um número!")
            input("Pressione ENTER para continuar...")
            return
        
        confirm = input(f"{Colors.YELLOW}Tem certeza? (s/n): {Colors.ENDC}").strip().lower()
        if confirm != "s":
            print_warning("Operação cancelada.")
            input("Pressione ENTER para continuar...")
            return
        
        response = requests.delete(f"{API_BASE_URL}/users/{user_id}", timeout=TIMEOUT)
        
        if response.status_code == 204:
            print_success("Usuário deletado com sucesso!")
        else:
            print_error(f"Erro ao deletar usuário: {response.text}")
    
    except requests.exceptions.ConnectionError:
        print_error("Não foi possível conectar à API. Verifique se o servidor está rodando.")
    except Exception as e:
        print_error(f"Erro: {str(e)}")
    
    input("\nPressione ENTER para continuar...")

def menu_agendamentos():
    """Menu de gerenciamento de agendamentos."""
    while True:
        clear_screen()
        print_header("GERENCIAMENTO DE AGENDAMENTOS")
        print(f"{Colors.BOLD}O que deseja fazer?{Colors.ENDC}\n")
        print("  1. Criar novo agendamento")
        print("  2. Listar agendamentos")
        print("  3. Filtrar agendamentos")
        print("  4. Exportar agendamentos para CSV")
        print("  5. Consultar minutos reservados")
        print("  6. Voltar ao menu principal\n")
        
        choice = input(f"{Colors.BOLD}Escolha uma opção (1-6): {Colors.ENDC}").strip()
        
        if choice == "1":
            criar_agendamento()
        elif choice == "2":
            listar_agendamentos()
        elif choice == "3":
            filtrar_agendamentos()
        elif choice == "4":
            exportar_agendamentos()
        elif choice == "5":
            consultar_minutos_reservados()
        elif choice == "6":
            break
        else:
            print_error("Opção inválida!")
            input("Pressione ENTER para continuar...")

def criar_agendamento():
    """Cria um novo agendamento."""
    clear_screen()
    print_header("CRIAR NOVO AGENDAMENTO")
    
    try:
        user_id = input(f"{Colors.BOLD}ID do usuário: {Colors.ENDC}").strip()
        if not user_id.isdigit():
            print_error("ID do usuário deve ser um número!")
            input("Pressione ENTER para continuar...")
            return
        
        resource_id = input(f"{Colors.BOLD}ID do recurso: {Colors.ENDC}").strip()
        if not resource_id.isdigit():
            print_error("ID do recurso deve ser um número!")
            input("Pressione ENTER para continuar...")
            return
        
        print(f"\n{Colors.BOLD}Data e hora de início:{Colors.ENDC}")
        print("Formato: YYYY-MM-DD HH:MM:SS (ex: 2025-11-14 10:00:00)")
        start_time = input(f"{Colors.BOLD}Data/hora: {Colors.ENDC}").strip()
        
        try:
            datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            print_error("Formato de data/hora inválido!")
            input("Pressione ENTER para continuar...")
            return
        
        duration = input(f"{Colors.BOLD}Duração em minutos: {Colors.ENDC}").strip()
        if not duration.isdigit() or int(duration) <= 0:
            print_error("Duração deve ser um número positivo!")
            input("Pressione ENTER para continuar...")
            return
        
        notes = input(f"{Colors.BOLD}Notas (opcional): {Colors.ENDC}").strip()
        
        payload = {
            "user_id": int(user_id),
            "resource_id": int(resource_id),
            "start_time": start_time,
            "duration_minutes": int(duration),
            "notes": notes or None
        }
        
        response = requests.post(f"{API_BASE_URL}/appointments", json=payload, timeout=TIMEOUT)
        
        if response.status_code == 200:
            appt = response.json()
            print_success("Agendamento criado com sucesso!")
            print(f"\n{Colors.BOLD}ID:{Colors.ENDC} {appt['id']}")
            print(f"{Colors.BOLD}Usuário:{Colors.ENDC} {appt['user_id']}")
            print(f"{Colors.BOLD}Recurso:{Colors.ENDC} {appt['resource_id']}")
            print(f"{Colors.BOLD}Início:{Colors.ENDC} {appt['start_time']}")
            print(f"{Colors.BOLD}Fim:{Colors.ENDC} {appt['end_time']}")
            print(f"{Colors.BOLD}Status:{Colors.ENDC} {appt['status']}")
        else:
            error_detail = response.json().get('detail', response.text)
            print_error(f"Erro ao criar agendamento: {error_detail}")
    
    except requests.exceptions.ConnectionError:
        print_error("Não foi possível conectar à API. Verifique se o servidor está rodando.")
    except Exception as e:
        print_error(f"Erro: {str(e)}")
    
    input("\nPressione ENTER para continuar...")

def listar_agendamentos():
    """Lista todos os agendamentos."""
    clear_screen()
    print_header("LISTAR AGENDAMENTOS")
    
    try:
        response = requests.get(f"{API_BASE_URL}/appointments", timeout=TIMEOUT)
        
        if response.status_code == 200:
            appointments = response.json()
            
            if not appointments:
                print_warning("Nenhum agendamento encontrado.")
            else:
                print(f"{Colors.BOLD}Total: {len(appointments)} agendamento(s){Colors.ENDC}\n")
                print(f"{Colors.BOLD}{'ID':<5} {'Usuário':<8} {'Recurso':<8} {'Início':<20} {'Status':<12}{Colors.ENDC}")
                print("-" * 60)
                
                for appt in appointments:
                    print(f"{appt['id']:<5} {appt['user_id']:<8} {appt['resource_id']:<8} {appt['start_time']:<20} {appt['status']:<12}")
        else:
            print_error(f"Erro ao listar agendamentos: {response.text}")
    
    except requests.exceptions.ConnectionError:
        print_error("Não foi possível conectar à API. Verifique se o servidor está rodando.")
    except Exception as e:
        print_error(f"Erro: {str(e)}")
    
    input("\nPressione ENTER para continuar...")

def filtrar_agendamentos():
    """Filtra agendamentos por critérios."""
    clear_screen()
    print_header("FILTRAR AGENDAMENTOS")
    
    try:
        print(f"{Colors.BOLD}Filtros disponíveis (deixe em branco para pular):{Colors.ENDC}\n")
        
        user_id = input("ID do usuário (opcional): ").strip()
        start_date = input("Data de início (YYYY-MM-DD HH:MM:SS, opcional): ").strip()
        end_date = input("Data de fim (YYYY-MM-DD HH:MM:SS, opcional): ").strip()
        order_by = input("Ordenar por (start_time/status, padrão: start_time): ").strip() or "start_time"
        
        params = {}
        if user_id and user_id.isdigit():
            params["user_id"] = int(user_id)
        if start_date:
            params["start"] = start_date
        if end_date:
            params["end"] = end_date
        params["order_by"] = order_by
        
        response = requests.get(f"{API_BASE_URL}/appointments", params=params, timeout=TIMEOUT)
        
        if response.status_code == 200:
            appointments = response.json()
            
            if not appointments:
                print_warning("Nenhum agendamento encontrado com esses filtros.")
            else:
                print(f"\n{Colors.BOLD}Total: {len(appointments)} agendamento(s){Colors.ENDC}\n")
                print(f"{Colors.BOLD}{'ID':<5} {'Usuário':<8} {'Recurso':<8} {'Início':<20} {'Status':<12}{Colors.ENDC}")
                print("-" * 60)
                
                for appt in appointments:
                    print(f"{appt['id']:<5} {appt['user_id']:<8} {appt['resource_id']:<8} {appt['start_time']:<20} {appt['status']:<12}")
        else:
            print_error(f"Erro ao filtrar agendamentos: {response.text}")
    
    except requests.exceptions.ConnectionError:
        print_error("Não foi possível conectar à API. Verifique se o servidor está rodando.")
    except Exception as e:
        print_error(f"Erro: {str(e)}")
    
    input("\nPressione ENTER para continuar...")

def exportar_agendamentos():
    """Exporta agendamentos para CSV."""
    clear_screen()
    print_header("EXPORTAR AGENDAMENTOS")
    
    try:
        response = requests.get(f"{API_BASE_URL}/appointments/export", timeout=TIMEOUT)
        
        if response.status_code == 200:
            result = response.json()
            path = result.get("path", "Desconhecido")
            print_success(f"Agendamentos exportados com sucesso!")
            print(f"\n{Colors.BOLD}Arquivo:{Colors.ENDC} {path}")
        else:
            print_error(f"Erro ao exportar: {response.text}")
    
    except requests.exceptions.ConnectionError:
        print_error("Não foi possível conectar à API. Verifique se o servidor está rodando.")
    except Exception as e:
        print_error(f"Erro: {str(e)}")
    
    input("\nPressione ENTER para continuar...")

def consultar_minutos_reservados():
    """Consulta minutos reservados de um usuário."""
    clear_screen()
    print_header("CONSULTAR MINUTOS RESERVADOS")
    
    try:
        user_id = input(f"{Colors.BOLD}ID do usuário: {Colors.ENDC}").strip()
        
        if not user_id.isdigit():
            print_error("ID deve ser um número!")
            input("Pressione ENTER para continuar...")
            return
        
        response = requests.get(f"{API_BASE_URL}/users/{user_id}/reserved_minutes", timeout=TIMEOUT)
        
        if response.status_code == 200:
            result = response.json()
            minutes = result.get("reserved_minutes", 0)
            hours = minutes // 60
            remaining_minutes = minutes % 60
            
            print_success(f"Usuário {user_id} tem {minutes} minutos reservados")
            print(f"\n{Colors.BOLD}Total:{Colors.ENDC} {hours}h {remaining_minutes}min")
        else:
            print_error(f"Erro: {response.text}")
    
    except requests.exceptions.ConnectionError:
        print_error("Não foi possível conectar à API. Verifique se o servidor está rodando.")
    except Exception as e:
        print_error(f"Erro: {str(e)}")
    
    input("\nPressione ENTER para continuar...")

def menu_relatorios():
    """Menu de relatórios."""
    while True:
        clear_screen()
        print_header("RELATÓRIOS")
        print(f"{Colors.BOLD}O que deseja visualizar?{Colors.ENDC}\n")
        print("  1. Resumo do sistema")
        print("  2. Voltar ao menu principal\n")
        
        choice = input(f"{Colors.BOLD}Escolha uma opção (1-2): {Colors.ENDC}").strip()
        
        if choice == "1":
            visualizar_resumo()
        elif choice == "2":
            break
        else:
            print_error("Opção inválida!")
            input("Pressione ENTER para continuar...")

def visualizar_resumo():
    """Visualiza um resumo do sistema."""
    clear_screen()
    print_header("RESUMO DO SISTEMA")
    
    try:
        # Total de agendamentos
        resp_appts = requests.get(f"{API_BASE_URL}/appointments", timeout=TIMEOUT)
        if resp_appts.status_code == 200:
            appts = resp_appts.json()
            print(f"{Colors.BOLD}Total de Agendamentos:{Colors.ENDC} {len(appts)}")
        
        print_success("Relatório gerado com sucesso!")
    
    except requests.exceptions.ConnectionError:
        print_error("Não foi possível conectar à API. Verifique se o servidor está rodando.")
    except Exception as e:
        print_error(f"Erro: {str(e)}")
    
    input("\nPressione ENTER para continuar...")

def main():
    """Loop principal da aplicação."""
    while True:
        choice = menu_principal()
        
        if choice == "1":
            menu_usuarios()
        elif choice == "2":
            menu_agendamentos()
        elif choice == "3":
            menu_relatorios()
        elif choice == "4":
            clear_screen()
            print_success("Até logo!")
            sys.exit(0)
        else:
            print_error("Opção inválida!")
            input("Pressione ENTER para continuar...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print_warning("\nAplicação interrompida pelo usuário.")
        sys.exit(0)
