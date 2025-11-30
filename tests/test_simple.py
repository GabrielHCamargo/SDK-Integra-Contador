"""
Teste simples para verificar se o SDK funciona corretamente.

Este arquivo demonstra como usar o SDK Integra Contador para fazer chamadas à API.
Execute este arquivo para testar a funcionalidade básica do SDK.

IMPORTANTE: Antes de executar, configure:
1. O token Bearer válido na variável TOKEN
2. Os dados de contratante, contribuinte e autorPedidoDados corretos
"""

import asyncio

from integra_sdk import IntegraClient
from integra_sdk.exceptions import (
    APIError,
    HTTPError,
    RequestNotFoundError,
    ValidationError,
)


async def test_consultar_caixapostal():
    """
    Teste 1: Consultar detalhes de mensagem (CAIXAPOSTAL)

    Este teste demonstra como usar o método consultar() para obter
    detalhes de uma mensagem específica do sistema CAIXAPOSTAL.
    """
    print("\n" + "=" * 60)
    print("TESTE 1: Consultar Detalhes de Mensagem (CAIXAPOSTAL)")
    print("=" * 60)

    # Configuração do cliente
    # IMPORTANTE: Substitua pelos valores reais
    config = {
        "contratante": {"numero": "00000000000000", "tipo": 2},  # CNPJ
        "contribuinte": {"numero": "00000000000000", "tipo": 2},  # CNPJ
        "autorPedidoDados": {"numero": "00000000000000", "tipo": 2},  # CNPJ
    }

    # Dados para a consulta
    dados = {"isn": "0000082838"}  # Número de identificação da mensagem

    try:
        # Criar cliente e fazer a requisição
        # Em Trial, o token é opcional (usa token fixo automaticamente)
        async with IntegraClient("Trial", config) as client:
            print(f"\nFazendo requisição para CAIXAPOSTAL/MSGDETALHAMENTO62...")
            print(f"Dados: {dados}")

            response = await client.consultar(
                id_sistema="CAIXAPOSTAL", id_servico="MSGDETALHAMENTO62", dados=dados
            )

            print("\n[OK] Sucesso! Resposta recebida:")
            print(f"\nStatus: {response.get('status')}")
            print(f"\nMensagens da API:")
            for msg in response.get("mensagens", []):
                print(f"  - {msg.get('codigo')}: {msg.get('texto')}")

            dados_parsed = response.get("dados", {})
            if dados_parsed:
                print(f"\nDados parseados:")
                print(f"  Código: {dados_parsed.get('codigo')}")
                print(f"  Sucesso: {dados_parsed.get('sucesso')}")
                if dados_parsed.get("mensagens"):
                    print(
                        f"  Total de mensagens: {len(dados_parsed.get('mensagens', []))}"
                    )
                    primeira_msg = dados_parsed.get("mensagens", [])[0]
                    print(f"\n  Primeira mensagem:")
                    print(f"    Assunto: {primeira_msg.get('assunto', 'N/A')}")
                    print(f"    Data Envio: {primeira_msg.get('data_envio', 'N/A')}")
                    print(
                        f"    Data Leitura: {primeira_msg.get('data_leitura', 'N/A')}"
                    )

            print(f"\nResposta completa (estruturada):")
            import json

            print(json.dumps(response, indent=2, ensure_ascii=False))

    except RequestNotFoundError as e:
        print(f"\n[ERRO] Erro: Template não encontrado")
        print(f"  {e}")
    except ValidationError as e:
        print(f"\n[ERRO] Erro: Dados inválidos")
        print(f"  {e}")
        if hasattr(e, "errors"):
            print(f"  Detalhes: {e.errors}")
    except APIError as e:
        print(f"\n[ERRO] Erro da API")
        print(f"  Status: {e.status_code}")
        print(f"  Mensagem: {e}")
        if e.response_body:
            print(f"  Resposta: {e.response_body}")
    except HTTPError as e:
        print(f"\n[ERRO] Erro HTTP")
        print(f"  Status: {e.status_code}")
        print(f"  Mensagem: {e}")
    except Exception as e:
        print(f"\n[ERRO] Erro inesperado: {type(e).__name__}")
        print(f"  {e}")


async def test_emitir_dctfweb():
    """
    Teste 2: Gerar guia de arrecadação (DCTFWEB)

    Este teste demonstra como usar o método emitir() para gerar
    um documento de arrecadação do sistema DCTFWEB.
    """
    print("\n" + "=" * 60)
    print("TESTE 2: Gerar Guia de Arrecadação (DCTFWEB)")
    print("=" * 60)

    # Configuração do cliente
    config = {
        "contratante": {"numero": "00000000000000", "tipo": 2},
        "contribuinte": {"numero": "00000000000000", "tipo": 2},
        "autorPedidoDados": {"numero": "00000000000000", "tipo": 2},
    }

    # Dados para emissão da guia
    dados = {
        "categoria": "GERAL_MENSAL",
        "anoPA": "2027",
        "mesPA": "11",
        "numeroReciboEntrega": 24573,
    }

    try:
        # Em Trial, o token é opcional (usa token fixo automaticamente)
        async with IntegraClient("Trial", config) as client:
            print(f"\nFazendo requisição para DCTFWEB/GERARGUIA31...")
            print(f"Dados: {dados}")

            response = await client.emitir(
                id_sistema="DCTFWEB", id_servico="GERARGUIA31", dados=dados
            )

            print("\n[OK] Sucesso! Resposta recebida:")
            print(f"Response: {response}")

    except ValidationError as e:
        print(f"\n[ERRO] Erro: Dados inválidos")
        print(f"  {e}")
        if hasattr(e, "errors"):
            print(f"  Detalhes: {e.errors}")
    except APIError as e:
        print(f"\n[ERRO] Erro da API")
        print(f"  Status: {e.status_code}")
        print(f"  Mensagem: {e}")
    except Exception as e:
        print(f"\n[ERRO] Erro: {type(e).__name__}")
        print(f"  {e}")


async def test_validacao_erro():
    """
    Teste 3: Validação de dados (teste de erro)

    Este teste demonstra como o SDK valida os dados antes de enviar
    a requisição, capturando erros de validação.
    """
    print("\n" + "=" * 60)
    print("TESTE 3: Validação de Dados (Teste de Erro)")
    print("=" * 60)

    config = {
        "contratante": {"numero": "00000000000000", "tipo": 2},
        "contribuinte": {"numero": "00000000000000", "tipo": 2},
        "autorPedidoDados": {"numero": "00000000000000", "tipo": 2},
    }

    # Dados inválidos (sem o campo obrigatório 'isn')
    dados_invalidos = {}

    try:
        # Em Trial, o token é opcional (usa token fixo automaticamente)
        async with IntegraClient("Trial", config) as client:
            print(f"\nTentando fazer requisição com dados inválidos...")
            print(f"Dados: {dados_invalidos}")

            response = await client.consultar(
                id_sistema="CAIXAPOSTAL",
                id_servico="MSGDETALHAMENTO62",
                dados=dados_invalidos,
            )

            print("\n[ERRO] Erro: Deveria ter lançado ValidationError")

    except ValidationError as e:
        print("\n[OK] Sucesso! Validação funcionou corretamente")
        print(f"  Erro capturado: {e}")
        if hasattr(e, "errors"):
            print(f"  Detalhes: {e.errors}")
    except Exception as e:
        print(f"\n[ERRO] Erro inesperado: {type(e).__name__}")
        print(f"  {e}")


async def test_trial_production_tokens():
    """
    Teste 4: Validação de tokens em Trial e Produção

    Este teste valida o comportamento do SDK com tokens:
    - Trial sem token: usa token fixo automaticamente
    - Trial com token: usa o token fornecido
    - Produção sem token: deve lançar erro
    - Produção com token: funciona normalmente
    """
    print("\n" + "=" * 60)
    print("TESTE 4: Validação de Tokens (Trial vs Produção)")
    print("=" * 60)

    config = {
        "contratante": {"numero": "00000000000000", "tipo": 2},
        "contribuinte": {"numero": "00000000000000", "tipo": 2},
        "autorPedidoDados": {"numero": "00000000000000", "tipo": 2},
    }

    # Teste 1: Trial sem token (deve usar token fixo)
    print("\n[TESTE 1] Trial sem token fornecido...")
    try:
        async with IntegraClient("Trial", config) as client:
            print("  ✓ Cliente criado com sucesso (usando token fixo)")
            print(f"  Token usado: {client.config.token[:20]}...")
    except Exception as e:
        print(f"  ✗ Erro inesperado: {e}")

    # Teste 2: Trial com token customizado
    print("\n[TESTE 2] Trial com token customizado...")
    try:
        custom_token = "token-customizado-teste"
        async with IntegraClient("Trial", config, token=custom_token) as client:
            print("  ✓ Cliente criado com sucesso (usando token customizado)")
            print(f"  Token usado: {client.config.token}")
            if client.config.token == custom_token:
                print("  ✓ Token customizado foi aplicado corretamente")
            else:
                print("  ✗ Token customizado não foi aplicado")
    except Exception as e:
        print(f"  ✗ Erro inesperado: {e}")

    # Teste 3: Produção sem token (deve lançar erro)
    print("\n[TESTE 3] Produção sem token (deve falhar)...")
    try:
        async with IntegraClient("Production", config) as client:
            print("  ✗ ERRO: Deveria ter lançado ValueError")
    except ValueError as e:
        print(f"  ✓ Erro esperado capturado: {e}")
    except Exception as e:
        print(f"  ✗ Erro inesperado: {type(e).__name__}: {e}")

    # Teste 4: Produção com token
    print("\n[TESTE 4] Produção com token...")
    try:
        production_token = "token-producao-teste"
        async with IntegraClient(
            "Production", config, token=production_token
        ) as client:
            print("  ✓ Cliente criado com sucesso")
            print(f"  Token usado: {client.config.token}")
            if client.config.token == production_token:
                print("  ✓ Token de produção foi aplicado corretamente")
            else:
                print("  ✗ Token de produção não foi aplicado")
    except Exception as e:
        print(f"  ✗ Erro inesperado: {type(e).__name__}: {e}")

    print("\n" + "=" * 60)


async def main():
    """
    Função principal que executa todos os testes.

    Execute este arquivo para rodar os testes:
        python tests/test_simple.py
    """
    print("\n" + "=" * 60)
    print("TESTES DO SDK INTEGRA CONTADOR")
    print("=" * 60)
    print("\nIMPORTANTE:")
    print("1. Em Trial, o token é opcional (usa token fixo automaticamente)")
    print("2. Em Produção, o token é obrigatório")
    print("3. Configure os dados de contratante/contribuinte corretos")
    print("\n" + "=" * 60)

    # Executa os testes
    # Descomente os testes que deseja executar:

    # Teste 1: Consultar CAIXAPOSTAL
    await test_consultar_caixapostal()

    # Teste 2: Emitir DCTFWEB
    # await test_emitir_dctfweb()

    # Teste 3: Validação (sempre funciona, não precisa de token)
    # await test_validacao_erro()

    # Teste 4: Validação de tokens (Trial vs Produção)
    # await test_trial_production_tokens()

    print("\n" + "=" * 60)
    print("TESTES CONCLUÍDOS")
    print("=" * 60)


if __name__ == "__main__":
    # Executa os testes
    asyncio.run(main())
