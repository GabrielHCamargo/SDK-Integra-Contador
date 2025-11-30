# SDK Integra Contador

SDK local para comunicação padronizada com a API Integra Contador. Este SDK fornece uma interface Python tipada e segura para interagir com os diversos sistemas e serviços da API.

**Autor**: Gabriel Camargo  
**Licença**: [Apache License 2.0](LICENSE)

## Características

- **Templates Python tipados**: Validação de dados em tempo de execução usando Pydantic
- **Interface simples**: API limpa e intuitiva para os microsserviços
- **Dados no formato original**: Retorna os dados exatamente como a API fornece, sem transformações
- **Tratamento de erros**: Exceções específicas e descritivas
- **Retry automático**: Retentativas automáticas para falhas de rede
- **Extensível**: Sistema de templates fácil de estender

## Instalação

### Requisitos

- Python 3.9 ou superior
- pip (gerenciador de pacotes Python)

### Instalação via Git (Recomendado)

Para instalar o SDK diretamente do repositório GitHub:

```bash
pip install git+https://github.com/GabrielHCamargo/SDK-Integra-Contador.git
```

Esta é a forma mais simples e recomendada para uso em produção. O pip irá baixar o código do repositório e instalar o SDK com todas as suas dependências.

#### Instalação em Modo Desenvolvimento

Se você deseja fazer alterações no código do SDK ou contribuir com o projeto:

```bash
git clone https://github.com/GabrielHCamargo/SDK-Integra-Contador.git
cd SDK-Integra-Contador
pip install -e .
```

O modo de desenvolvimento (`-e` ou `--editable`) permite que você faça alterações no código e elas sejam refletidas imediatamente sem precisar reinstalar o pacote.

### Instalação Local

Se você já tem o código do SDK localmente:

```bash
cd SDK-Integra-Contador
pip install -e .  # Modo desenvolvimento (recomendado para desenvolvimento)
```

Ou, para instalação em modo produção (sem edição):

```bash
cd SDK-Integra-Contador
pip install .
```

### Dependências

O SDK instala automaticamente as seguintes dependências:

**Dependências principais:**

- `pydantic==2.12.5` - Validação de dados e modelos tipados
- `httpx==0.28.1` - Cliente HTTP assíncrono para requisições à API
- `typing-extensions==4.15.0` - Extensões de tipagem para Python

**Dependências para autenticação:**

- `requests>=2.32.0` - Cliente HTTP síncrono (usado para autenticação com certificado)
- `requests-pkcs12>=1.27.0` - Suporte para certificados PKCS12 na autenticação

Todas as dependências são instaladas automaticamente quando você instala o SDK usando `pip install`.

### Verificação da Instalação

Para verificar se o SDK foi instalado corretamente:

```bash
python -c "import integra_sdk; print(integra_sdk.__version__)"
```

Você deve ver a versão do SDK impressa (ex: `0.1.0`).

### Diretório de Autenticação (`.auth/`)

O SDK gerencia automaticamente as credenciais e tokens de autenticação no diretório `.auth/` localizado na raiz do pacote SDK:

- **Localização**: `integra_sdk/.auth/`
- **Arquivos salvos**:
  - `config.json` - Armazena as credenciais de autenticação (consumer_key, consumer_secret, certificate_path, etc.)
  - `token.json` - Armazena o token de acesso e informações de expiração

**Importante**:

- O diretório `.auth/` é criado automaticamente na primeira autenticação
- As credenciais são salvas apenas quando você usa autenticação por certificado digital
- Em sessões futuras, o SDK carrega automaticamente as credenciais salvas
- Os tokens são renovados automaticamente quando expirados
- **Não commite o diretório `.auth/` no controle de versão** (já está no `.gitignore`)

## Uso Básico

### Configuração Inicial

```python
import asyncio
from integra_sdk import IntegraClient
from integra_sdk.exceptions import RequestNotFoundError, ValidationError, APIError

# Configuração usada em todas as operações
config = {
    "contratante": {"numero": "12345678000190", "tipo": 2},
    "contribuinte": {"numero": "12345678000190", "tipo": 2},
    "autorPedidoDados": {"numero": "12345678000190", "tipo": 2}
}
```

### Ambientes: Trial vs Produção

O SDK suporta dois ambientes com comportamentos diferentes para tokens:

#### Ambiente Trial

- **Token opcional**: Se não fornecido, usa automaticamente o token fixo de Trial
- **Token customizado**: Você pode fornecer um token específico se necessário

```python
# Trial sem token (usa token fixo automaticamente)
client = IntegraClient("Trial", config)

# Trial com token customizado (opcional)
client = IntegraClient("Trial", config, token="seu-token-customizado")
```

#### Ambiente Produção

O ambiente Production suporta autenticação com certificado digital e gerenciamento automático de tokens:

- **Autenticação com Certificado**: Requer `consumer_key`, `consumer_secret`, `certificate_path` e `certificate_password`
- **Persistência Automática**: As credenciais são salvas automaticamente no diretório `.auth/` do SDK
- **Carregamento Automático**: Em sessões futuras, as credenciais salvas são carregadas automaticamente
- **Renovação Automática de Token**: Tokens expirados são renovados automaticamente

```python
# Produção com autenticação por certificado (primeira vez - salva credenciais)
client = IntegraClient(
    "Production",
    config,
    consumer_key="sua-consumer-key",
    consumer_secret="sua-consumer-secret",
    certificate_path="caminho/para/certificado.p12",
    certificate_password="senha-do-certificado"
)

# Produção em sessões futuras (carrega credenciais salvas automaticamente)
# Não precisa fornecer credenciais novamente!
client = IntegraClient("Production", config)

# Produção com token estático (alternativa, não salva credenciais)
token = "seu-token-de-producao"
client = IntegraClient("Production", config, token=token)
```

**Nota**: As credenciais são salvas em `integra_sdk/.auth/config.json` e os tokens em `integra_sdk/.auth/token.json`. O SDK verifica automaticamente se o token está expirado e renova quando necessário.

### Exemplo 1: Consultar Detalhes de Mensagem (CAIXAPOSTAL)

```python
async def exemplo_consultar():
    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            response = await client.consultar(
                id_sistema="CAIXAPOSTAL",
                id_servico="MSGDETALHAMENTO62",
                dados={"isn": "0000082838"}
            )
            print(response)
        except RequestNotFoundError as e:
            print(f"Template não encontrado: {e}")
        except ValidationError as e:
            print(f"Dados inválidos: {e}")
        except APIError as e:
            print(f"Erro da API: {e}")

asyncio.run(exemplo_consultar())
```

### Exemplo 2: Listar Mensagens por Contribuinte (CAIXAPOSTAL)

```python
async def exemplo_listar_mensagens():
    """Exemplo de listagem de mensagens por contribuinte."""
    from integra_sdk import IntegraClient
    from integra_sdk.exceptions import ValidationError, APIError

    config = {}

    async with IntegraClient("Trial", config) as client:
        try:
            # Listar mensagens (todos os campos são opcionais)
            response = await client.consultar(
                id_sistema="CAIXAPOSTAL",
                id_servico="MSGCONTRIBUINTE61",
                dados={
                    "statusLeitura": "0",  # "0" = todas, "1" = não lidas, "2" = lidas
                    "indicadorPagina": "0",  # "0" = primeira página
                    "ponteiroPagina": "00000000000000",  # Ponteiro inicial
                }
            )

            # Os dados são retornados no formato original da API
            dados = response.get("dados", {})
            if dados:
                conteudo = dados.get("conteudo", [])
                if conteudo:
                    primeira_pagina = conteudo[0]
                    quantidade = primeira_pagina.get("quantidadeMensagens")
                    lista_mensagens = primeira_pagina.get("listaMensagens", [])
                    print(f"Quantidade de mensagens: {quantidade}")
                    print(f"Mensagens retornadas: {len(lista_mensagens)}")

                    # Exemplo de acesso aos campos originais
                    for msg in lista_mensagens[:3]:  # Mostrar apenas as 3 primeiras
                        print(f"\nMensagem:")
                        print(f"  - Código Sistema Remetente: {msg.get('codigoSistemaRemetente')}")
                        print(f"  - Assunto: {msg.get('assuntoModelo')}")
                        print(f"  - Data Envio: {msg.get('dataEnvio')}")
                        print(f"  - Indicador Leitura: {msg.get('indicadorLeitura')}")

                    # Verificar se há próxima página
                    indicador_ultima = primeira_pagina.get("indicadorUltimaPagina")
                    if indicador_ultima == "N":
                        ponteiro_proxima = primeira_pagina.get("ponteiroProximaPagina")
                        print(f"\nHá mais páginas. Ponteiro próxima página: {ponteiro_proxima}")
        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e}")

asyncio.run(exemplo_listar_mensagens())
```

### Exemplo 3: Consultar CNPJ MEI Vinculado ao CPF (CCMEI)

```python
async def exemplo_consultar_cnpj_mei():
    """Exemplo de consulta da situação cadastral dos CNPJ MEI vinculados ao CPF."""
    from integra_sdk import IntegraClient
    from integra_sdk.exceptions import ValidationError, APIError

    config = {}

    async with IntegraClient("Trial", config) as client:
        try:
            # Consultar CNPJ MEI vinculado ao CPF
            # O CPF é determinado pelo campo contribuinte na requisição
            # Este serviço não requer dados de entrada (dados vazio)
            response = await client.consultar(
                id_sistema="CCMEI",
                id_servico="CCMEISITCADASTRAL123",
                dados={}  # Dados vazios - CPF vem do contribuinte
            )

            # Os dados são retornados no formato original da API (array JSON)
            dados = response.get("dados", [])
            if dados:
                print(f"Total de CNPJs encontrados: {len(dados)}")

                # Exemplo de acesso aos campos originais
                for cnpj_info in dados:
                    cnpj = cnpj_info.get("cnpj")
                    situacao = cnpj_info.get("situacao")
                    enquadrado_mei = cnpj_info.get("enquadradoMei")

                    print(f"\nCNPJ: {cnpj}")
                    print(f"  - Situação: {situacao}")
                    print(f"  - Enquadrado MEI: {enquadrado_mei}")
        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e}")

asyncio.run(exemplo_consultar_cnpj_mei())
```

### Exemplo 4: Consultar Certificado MEI (CCMEI)

```python
async def exemplo_consultar_certificado_mei():
    """Exemplo de consulta dos dados do Certificado de Condição MEI."""
    from integra_sdk import IntegraClient
    from integra_sdk.exceptions import ValidationError, APIError

    config = {}

    async with IntegraClient("Trial", config) as client:
        try:
            # Consultar dados do Certificado de Condição MEI
            # O CNPJ é determinado pelo campo contribuinte na requisição
            # Este serviço não requer dados de entrada (dados vazio)
            response = await client.consultar(
                id_sistema="CCMEI",
                id_servico="DADOSCCMEI122",
                dados={}  # Dados vazios - CNPJ vem do contribuinte
            )

            # Os dados são retornados no formato original da API
            dados = response.get("dados", {})
            if dados:
                # Exemplo de acesso aos campos originais
                cnpj = dados.get("cnpj")
                nome_empresarial = dados.get("nomeEmpresarial")
                situacao_cadastral = dados.get("situacaoCadastralVigente")
                data_inicio = dados.get("dataInicioAtividades")

                print(f"CNPJ: {cnpj}")
                print(f"Nome Empresarial: {nome_empresarial}")
                print(f"Situação Cadastral: {situacao_cadastral}")
                print(f"Data Início Atividades: {data_inicio}")

                # Empresário
                empresario = dados.get("empresario", {})
                if empresario:
                    print(f"\nEmpresário:")
                    print(f"  - Nome Civil: {empresario.get('nomeCivil')}")
                    print(f"  - CPF: {empresario.get('cpf')}")

                # Endereço
                endereco = dados.get("enderecoComercial", {})
                if endereco:
                    print(f"\nEndereço:")
                    print(f"  - {endereco.get('logradouro')}, {endereco.get('numero')}")
                    print(f"  - {endereco.get('bairro')} - {endereco.get('municipio')}/{endereco.get('uf')}")
                    print(f"  - CEP: {endereco.get('cep')}")

                # Enquadramento
                enquadramento = dados.get("enquadramento", {})
                if enquadramento:
                    print(f"\nEnquadramento:")
                    print(f"  - Situação: {enquadramento.get('situacao')}")
                    print(f"  - Optante MEI: {enquadramento.get('optanteMei')}")
        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e}")

asyncio.run(exemplo_consultar_certificado_mei())
```

### Exemplo 5: Emitir Certificado MEI em PDF (CCMEI)

```python
import base64

async def exemplo_emitir_certificado_mei():
    """Exemplo de emissão do Certificado de Condição de MEI em formato PDF."""
    from integra_sdk import IntegraClient
    from integra_sdk.exceptions import ValidationError, APIError

    config = {}

    async with IntegraClient("Trial", config) as client:
        try:
            # Emitir Certificado de Condição de MEI em formato PDF
            # O CNPJ é determinado pelo campo contribuinte na requisição
            # Este serviço não requer dados de entrada (dados vazio)
            response = await client.emitir(
                id_sistema="CCMEI",
                id_servico="EMITIRCCMEI121",
                dados={}  # Dados vazios - CNPJ vem do contribuinte
            )

            # Os dados são retornados no formato original da API (array JSON)
            dados = response.get("dados", [])
            if dados:
                # Exemplo de acesso aos campos originais
                for item in dados:
                    cnpj = item.get("cnpj")
                    pdf_base64 = item.get("pdf")

                    if pdf_base64:
                        # Decodificar o PDF de Base64
                        pdf_bytes = base64.b64decode(pdf_base64)

                        # Salvar o PDF em um arquivo
                        nome_arquivo = f"certificado_mei_{cnpj}.pdf"
                        with open(nome_arquivo, "wb") as f:
                            f.write(pdf_bytes)

                        print(f"Certificado emitido para CNPJ {cnpj}")
                        print(f"PDF salvo em: {nome_arquivo}")
        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e}")

asyncio.run(exemplo_emitir_certificado_mei())
```

### Exemplo 6: Gerar Guia de Arrecadação (DCTFWEB)

```python
async def exemplo_emitir():
    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            response = await client.emitir(
                id_sistema="DCTFWEB",
                id_servico="GERARGUIA31",
                dados={
                    "categoria": "GERAL_MENSAL",
                    "anoPA": "2027",
                    "mesPA": "11",
                    "numeroReciboEntrega": 24573
                }
            )
            print(response)
        except ValidationError as e:
            print(f"Dados inválidos: {e.errors}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_emitir())
```

### Exemplo 7: Consultar XML da Declaração (DCTFWEB)

```python
import base64

async def exemplo_consultar_xml():
    """Exemplo de consulta do XML da declaração."""
    from integra_sdk import IntegraClient
    from integra_sdk.exceptions import ValidationError, APIError

    config = {}

    async with IntegraClient("Trial", config) as client:
        try:
            # Consultar XML da Declaração
            response = await client.consultar(
                id_sistema="DCTFWEB",
                id_servico="CONSXMLDECLARACAO38",
                dados={
                    "categoria": "PF_MENSAL",
                    "anoPA": "2022",
                    "mesPA": "06"
                }
            )

            # Os dados são retornados no formato original da API
            dados = response.get("dados", {})

            # A resposta contém XMLStringBase64 com o XML em Base64
            if "XMLStringBase64" in dados:
                xml_base64 = dados["XMLStringBase64"]
                # Decodificar o XML
                xml_content = base64.b64decode(xml_base64).decode("utf-8")
                print("XML da Declaração:")
                print(xml_content)

            print(f"Status: {response.get('status')}")
            print(f"Mensagens: {response.get('mensagens', [])}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_consultar_xml())
```

### Exemplo 7.5: Gerar Guia em Andamento (DCTFWEB)

```python
import base64

async def exemplo_gerar_guia_andamento():
    """Exemplo de geração de guia em andamento."""
    from integra_sdk import IntegraClient
    from integra_sdk.exceptions import ValidationError, APIError

    config = {}

    async with IntegraClient("Trial", config) as client:
        try:
            # Gerar Guia em Andamento
            # Nota: similar ao GERARGUIA31, mas sem numeroReciboEntrega
            response = await client.emitir(
                id_sistema="DCTFWEB",
                id_servico="GERARGUIAANDAMENTO313",
                dados={
                    "categoria": "GERAL_MENSAL",
                    "anoPA": "2025",
                    "mesPA": "01"
                }
            )

            # Os dados são retornados no formato original da API
            dados = response.get("dados", {})

            # A resposta contém PDFByteArrayBase64 com o PDF em Base64
            if "PDFByteArrayBase64" in dados:
                pdf_base64 = dados["PDFByteArrayBase64"]
                # Decodificar o PDF
                pdf_content = base64.b64decode(pdf_base64)

                # Salvar o PDF em arquivo (opcional)
                with open("guia_andamento.pdf", "wb") as f:
                    f.write(pdf_content)

                print("PDF da guia salvo em 'guia_andamento.pdf'")

            print(f"Status: {response.get('status')}")
            print(f"Mensagens: {response.get('mensagens', [])}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_gerar_guia_andamento())
```

### Exemplo 8: Consultar Recibo de Transmissão (DCTFWEB)

```python
import base64

async def exemplo_consultar_recibo():
    """Exemplo de consulta do recibo de transmissão."""
    from integra_sdk import IntegraClient
    from integra_sdk.exceptions import ValidationError, APIError

    config = {}

    async with IntegraClient("Trial", config) as client:
        try:
            # Consultar Recibo de Transmissão
            # Nota: categoria é um número inteiro (ex: 40, 50), não string
            response = await client.consultar(
                id_sistema="DCTFWEB",
                id_servico="CONSRECIBO32",
                dados={
                    "categoria": 40,
                    "anoPA": "2027",
                    "mesPA": "11",
                    "numeroReciboEntrega": 24573
                }
            )

            # Os dados são retornados no formato original da API
            dados = response.get("dados", {})

            # A resposta contém PDFByteArrayBase64 com o PDF em Base64
            if "PDFByteArrayBase64" in dados:
                pdf_base64 = dados["PDFByteArrayBase64"]
                # Decodificar o PDF
                pdf_content = base64.b64decode(pdf_base64)

                # Salvar o PDF em arquivo (opcional)
                with open("recibo_transmissao.pdf", "wb") as f:
                    f.write(pdf_content)

                print("PDF do recibo salvo em 'recibo_transmissao.pdf'")

            print(f"Status: {response.get('status')}")
            print(f"Mensagens: {response.get('mensagens', [])}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_consultar_recibo())
```

### Exemplo 9: Consultar Relatório Declaração Completa (DCTFWEB)

```python
import base64

async def exemplo_consultar_relatorio():
    """Exemplo de consulta do relatório de declaração completa."""
    from integra_sdk import IntegraClient
    from integra_sdk.exceptions import ValidationError, APIError

    config = {}

    async with IntegraClient("Trial", config) as client:
        try:
            # Consultar Relatório Declaração Completa
            # Nota: categoria é uma string (ex: "GERAL_MENSAL")
            response = await client.consultar(
                id_sistema="DCTFWEB",
                id_servico="CONSDECCOMPLETA33",
                dados={
                    "categoria": "GERAL_MENSAL",
                    "anoPA": "2027",
                    "mesPA": "11",
                    "numeroReciboEntrega": 24573
                }
            )

            # Os dados são retornados no formato original da API
            dados = response.get("dados", {})

            # A resposta contém PDFByteArrayBase64 com o PDF em Base64
            if "PDFByteArrayBase64" in dados:
                pdf_base64 = dados["PDFByteArrayBase64"]
                # Decodificar o PDF
                pdf_content = base64.b64decode(pdf_base64)

                # Salvar o PDF em arquivo (opcional)
                with open("relatorio_declaracao_completa.pdf", "wb") as f:
                    f.write(pdf_content)

                print("PDF do relatório salvo em 'relatorio_declaracao_completa.pdf'")

            print(f"Status: {response.get('status')}")
            print(f"Mensagens: {response.get('mensagens', [])}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_consultar_relatorio())
```

### Exemplo 10: Transmitir Declaração (DCTFWEB)

```python
import base64

async def exemplo_transmitir_declaracao():
    """Exemplo de transmissão de declaração DCTF."""
    from integra_sdk import IntegraClient
    from integra_sdk.exceptions import ValidationError, APIError

    config = {}

    async with IntegraClient("Trial", config) as client:
        try:
            # Ler o XML assinado de um arquivo e codificar em Base64
            with open("declaracao_assinada.xml", "rb") as f:
                xml_content = f.read()
                xml_base64 = base64.b64encode(xml_content).decode("utf-8")

            # Transmitir Declaração
            # Nota: requer XML assinado em Base64
            response = await client.consultar(
                id_sistema="DCTFWEB",
                id_servico="TRANSDECLARACAO310",
                dados={
                    "categoria": "PF_MENSAL",
                    "anoPA": "2022",
                    "mesPA": "06",
                    "xmlAssinadoBase64": xml_base64
                }
            )

            # Os dados são retornados no formato original da API
            dados = response.get("dados", {})

            print(f"Status: {response.get('status')}")
            print(f"Mensagens: {response.get('mensagens', [])}")

            if dados:
                print(f"Dados da resposta: {dados}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_transmitir_declaracao())
```

### Exemplo 11: Entregar Defis (DEFIS)

```python
import base64

async def exemplo_entregar_defis():
    """Exemplo de entrega de declaração DEFIS."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            # Estrutura complexa de dados da declaração DEFIS
            dados = {
                "ano": 2021,
                "inatividade": 2,
                "situacaoEspecial": None,
                "empresa": {
                    "ganhoCapital": 10.0,
                    "qtdEmpregadoInicial": 20,
                    "qtdEmpregadoFinal": 0,
                    "lucroContabil": 20.0,
                    "receitaExportacaoDireta": 10.0,
                    "comerciaisExportadoras": [
                        {
                            "cnpjCompleto": "00000000000000",
                            "valor": 123.0
                        }
                    ],
                    "socios": [
                        {
                            "cpf": "00000000000",
                            "rendimentosIsentos": 50.0,
                            "rendimentosTributaveis": 20.0,
                            "participacaoCapitalSocial": 90.0,
                            "irRetidoFonte": 10.0
                        }
                    ],
                    "participacaoCotasTesouraria": 10.0,
                    "ganhoRendaVariavel": 10.0,
                    "doacoesCampanhaEleitoral": [
                        {
                            "cnpjBeneficiario": "00000000000000",
                            "tipoBeneficiario": 1,
                            "formaDoacao": 1,
                            "valor": 10.0
                        }
                    ],
                    "estabelecimentos": [
                        {
                            "cnpjCompleto": "00000000000000",
                            "totalDevolucoesCompras": 200.0,
                            "OperacoesInterestaduais": [
                                {
                                    "Uf": "SP",
                                    "Valor": 15.0,
                                    "TipoOperacao": 1
                                }
                            ],
                            "IssRetidosFonte": [
                                {
                                    "Uf": "SP",
                                    "CodigoMunicipio": 7107,
                                    "Valor": 20.0
                                }
                            ],
                            "estoqueInicial": 10.0,
                            "estoqueFinal": 20.0,
                            "aquisicoesMercadoInterno": 20.0,
                            "importacoes": 50.0,
                            "totalEntradas": 5000.0,
                            "totalDespesas": 10000.0
                        }
                    ]
                },
                "naoOptante": None
            }

            response = await client.declarar(
                id_sistema="DEFIS",
                id_servico="TRANSDECLARACAO141",
                dados=dados
            )

            # Resposta contém PDFs em base64 e ID da declaração
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                declaracao_pdf = dados_resposta.get("declaracaoPdf")
                recibo_pdf = dados_resposta.get("reciboPdf")
                id_defis = dados_resposta.get("idDefis")

                print(f"ID Defis: {id_defis}")
                if declaracao_pdf:
                    # Decodificar PDF se necessário
                    pdf_bytes = base64.b64decode(declaracao_pdf)
                    print(f"Declaração PDF recebida ({len(pdf_bytes)} bytes)")
                if recibo_pdf:
                    pdf_bytes = base64.b64decode(recibo_pdf)
                    print(f"Recibo PDF recebido ({len(pdf_bytes)} bytes)")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_entregar_defis())
```

### Exemplo 12: Consultar Declarações (DEFIS)

```python
async def exemplo_consultar_declaracoes():
    """Exemplo de consulta de todas as declarações DEFIS."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            # Este serviço não requer dados de entrada
            response = await client.consultar(
                id_sistema="DEFIS",
                id_servico="CONSDECLARACAO142",
                dados={}  # Dados vazios
            )

            # Resposta contém array de declarações
            dados_resposta = response.get("dados", [])
            if dados_resposta:
                # dados é um array JSON string, precisa ser parseado
                import json
                declaracoes = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta

                for decl in declaracoes:
                    print(f"Ano: {decl.get('anoCalendario')}")
                    print(f"ID Defis: {decl.get('idDefis')}")
                    print(f"Tipo: {decl.get('tipo')}")
                    print(f"Data/Hora: {decl.get('dataHora')}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_consultar_declaracoes())
```

### Exemplo 13: Consultar Última Declaração e Recibo (DEFIS)

```python
import base64

async def exemplo_consultar_ultima_declaracao():
    """Exemplo de consulta da última declaração DEFIS de um ano."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            response = await client.consultar(
                id_sistema="DEFIS",
                id_servico="CONSULTIMADECREC143",
                dados={"ano": 2021}
            )

            # Resposta contém PDFs em base64 e ID da declaração
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                declaracao_pdf = dados_resposta.get("declaracaoPdf")
                recibo_pdf = dados_resposta.get("reciboPdf")
                id_defis = dados_resposta.get("idDefis")

                print(f"ID Defis: {id_defis}")
                if declaracao_pdf:
                    pdf_bytes = base64.b64decode(declaracao_pdf)
                    print(f"Declaração PDF recebida ({len(pdf_bytes)} bytes)")
                if recibo_pdf:
                    pdf_bytes = base64.b64decode(recibo_pdf)
                    print(f"Recibo PDF recebido ({len(pdf_bytes)} bytes)")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_consultar_ultima_declaracao())
```

### Exemplo 14: Consultar Declaração e Recibo por ID (DEFIS)

```python
import base64

async def exemplo_consultar_declaracao_por_id():
    """Exemplo de consulta de declaração DEFIS específica por ID."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            response = await client.consultar(
                id_sistema="DEFIS",
                id_servico="CONSDECREC144",
                dados={"idDefis": "000000002021002"}
            )

            # Resposta contém PDFs em base64 e ID da declaração
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                declaracao_pdf = dados_resposta.get("declaracaoPdf")
                recibo_pdf = dados_resposta.get("reciboPdf")
                id_defis = dados_resposta.get("idDefis")

                print(f"ID Defis: {id_defis}")
                if declaracao_pdf:
                    pdf_bytes = base64.b64decode(declaracao_pdf)
                    print(f"Declaração PDF recebida ({len(pdf_bytes)} bytes)")
                if recibo_pdf:
                    pdf_bytes = base64.b64decode(recibo_pdf)
                    print(f"Recibo PDF recebido ({len(pdf_bytes)} bytes)")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_consultar_declaracao_por_id())
```

### Exemplo 15: Obter Indicador DTE (DTE)

```python
async def exemplo_obter_indicador_dte():
    """Exemplo de consulta do indicador DTE."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            # Este serviço não requer dados de entrada
            response = await client.consultar(
                id_sistema="DTE",
                id_servico="CONSULTASITUACAODTE111",
                dados={}  # Dados vazios
            )

            # Resposta contém indicador de enquadramento e status
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                # dados é um JSON string, precisa ser parseado
                import json
                dados_dict = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta

                indicador = dados_dict.get("indicadorEnquadramento")
                status = dados_dict.get("statusEnquadramento")

                print(f"Indicador de Enquadramento: {indicador}")
                print(f"Status de Enquadramento: {status}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_obter_indicador_dte())
```

### Exemplo 16: Consultar Processos por Interessado (E-PROCESSO)

```python
async def exemplo_consultar_processos_interessado():
    """Exemplo de consulta de processos por interessado."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            # Este serviço não requer dados de entrada
            response = await client.consultar(
                id_sistema="EPROCESSO",
                id_servico="CONSPROCPORINTER271",
                dados={}  # Dados vazios
            )

            # Resposta contém lista de processos
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                # dados pode ser um JSON string ou objeto
                import json
                processos = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta

                if isinstance(processos, list):
                    print(f"Total de processos encontrados: {len(processos)}")
                    for processo in processos:
                        print(f"Processo: {processo}")
                else:
                    print(f"Dados dos processos: {processos}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_consultar_processos_interessado())
```

### Exemplo 17: Solicitar Eventos de PF (EVENTOS ATUALIZACAO)

```python
async def exemplo_solicitar_eventos_pf():
    """Exemplo de solicitação de eventos de atualização para PF."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            response = await client.monitorar(
                id_sistema="EVENTOSATUALIZACAO",
                id_servico="SOLICEVENTOSPF131",
                dados={"evento": "E0301"}
            )

            # Resposta contém protocolo e informações de tempo
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                import json
                dados_dict = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta

                protocolo = dados_dict.get("protocolo")
                tempo_medio = dados_dict.get("TempoEsperaMedioEmMs")
                tempo_limite = dados_dict.get("TempoLimiteEmMin")

                print(f"Protocolo: {protocolo}")
                print(f"Tempo médio de espera: {tempo_medio}ms")
                print(f"Tempo limite: {tempo_limite} minutos")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_solicitar_eventos_pf())
```

### Exemplo 18: Obter Eventos de PF (EVENTOS ATUALIZACAO)

```python
async def exemplo_obter_eventos_pf():
    """Exemplo de obtenção de eventos de atualização para PF."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            # Primeiro solicite os eventos para obter o protocolo
            # Depois use o protocolo para obter os eventos
            response = await client.monitorar(
                id_sistema="EVENTOSATUALIZACAO",
                id_servico="OBTEREVENTOSPF133",
                dados={
                    "protocolo": "a65f3455-fa91-419b-b0ad-c4ac50695abf",
                    "evento": "E0301"
                }
            )

            # Resposta contém array de eventos
            dados_resposta = response.get("dados", [])
            if dados_resposta:
                import json
                eventos = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta

                if isinstance(eventos, list):
                    print(f"Total de eventos encontrados: {len(eventos)}")
                    for evento in eventos:
                        cpf = evento[0] if len(evento) > 0 else ""
                        data = evento[1] if len(evento) > 1 else ""
                        print(f"CPF: {cpf}, Data: {data}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_obter_eventos_pf())
```

### Exemplo 19: Solicitar Eventos de PJ (EVENTOS ATUALIZACAO)

```python
async def exemplo_solicitar_eventos_pj():
    """Exemplo de solicitação de eventos de atualização para PJ."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            response = await client.monitorar(
                id_sistema="EVENTOSATUALIZACAO",
                id_servico="SOLICEVENTOSPJ132",
                dados={"evento": "E0301"}
            )

            # Resposta contém protocolo e informações de tempo
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                import json
                dados_dict = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta

                protocolo = dados_dict.get("protocolo")
                tempo_medio = dados_dict.get("TempoEsperaMedioEmMs")
                tempo_limite = dados_dict.get("TempoLimiteEmMin")

                print(f"Protocolo: {protocolo}")
                print(f"Tempo médio de espera: {tempo_medio}ms")
                print(f"Tempo limite: {tempo_limite} minutos")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_solicitar_eventos_pj())
```

### Exemplo 20: Obter Eventos de PJ (EVENTOS ATUALIZACAO)

```python
async def exemplo_obter_eventos_pj():
    """Exemplo de obtenção de eventos de atualização para PJ."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            # Primeiro solicite os eventos para obter o protocolo
            # Depois use o protocolo para obter os eventos
            response = await client.monitorar(
                id_sistema="EVENTOSATUALIZACAO",
                id_servico="OBTEREVENTOSPJ134",
                dados={
                    "protocolo": "q90n3455-fa91-419c-c0ad-a4ms50215acl",
                    "evento": "E0301"
                }
            )

            # Resposta contém array de eventos
            dados_resposta = response.get("dados", [])
            if dados_resposta:
                import json
                eventos = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta

                if isinstance(eventos, list):
                    print(f"Total de eventos encontrados: {len(eventos)}")
                    for evento in eventos:
                        cnpj = evento[0] if len(evento) > 0 else ""
                        data = evento[1] if len(evento) > 1 else ""
                        print(f"CNPJ: {cnpj}, Data: {data}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_obter_eventos_pj())
```

### Exemplo 21: Encerrar Apuração (MIT)

```python
async def exemplo_encerrar_apuracao():
    """Exemplo de encerramento de apuração MIT."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            dados = {
                "PeriodoApuracao": {
                    "MesApuracao": 1,
                    "AnoApuracao": 2025
                },
                "DadosIniciais": {
                    "SemMovimento": False,
                    "QualificacaoPj": 1,
                    "TributacaoLucro": 2,
                    "VariacoesMonetarias": 1,
                    "RegimePisCofins": 1,
                    "ResponsavelApuracao": {
                        "CpfResponsavel": "00000000000"
                    }
                },
                "Debitos": {
                    "Irpj": {
                        "ListaDebitos": [{
                            "IdDebito": 1,
                            "CodigoDebito": "236208",
                            "CnpjScp": "88888888888888",
                            "ValorDebito": 100.00
                        }]
                    }
                }
            }

            response = await client.declarar(
                id_sistema="MIT",
                id_servico="ENCAPURACAO314",
                dados=dados
            )

            # Resposta contém protocoloEncerramento e idApuracao
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                import json
                dados_dict = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta

                protocolo = dados_dict.get("protocoloEncerramento")
                id_apuracao = dados_dict.get("idApuracao")

                print(f"Protocolo de encerramento: {protocolo}")
                print(f"ID da apuração: {id_apuracao}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_encerrar_apuracao())
```

### Exemplo 22: Consultar Situação do Encerramento (MIT)

```python
async def exemplo_consultar_situacao_encerramento():
    """Exemplo de consulta da situação do encerramento MIT."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            # Use o protocoloEncerramento retornado no encerramento
            response = await client.apoiar(
                id_sistema="MIT",
                id_servico="SITUACAOENC315",
                dados={"protocoloEncerramento": "AuYb4wuDp0GvCij3GDOAsA=="}
            )

            # Resposta contém situação da apuração
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                import json
                dados_dict = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta

                situacao = dados_dict.get("textoSituacao")
                id_apuracao = dados_dict.get("idApuracao")
                data_encerramento = dados_dict.get("dataEncerramento")

                print(f"Situação: {situacao}")
                print(f"ID da apuração: {id_apuracao}")
                print(f"Data de encerramento: {data_encerramento}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_consultar_situacao_encerramento())
```

### Exemplo 23: Consultar Apuração (MIT)

```python
async def exemplo_consultar_apuracao():
    """Exemplo de consulta de apuração MIT."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            # Use o idApuracao retornado no encerramento
            response = await client.consultar(
                id_sistema="MIT",
                id_servico="CONSAPURACAO316",
                dados={"IdApuracao": 0}
            )

            # Resposta contém dados completos da apuração
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                import json
                dados_dict = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta

                situacao = dados_dict.get("textoSituacao")
                dados_apuracao = dados_dict.get("dadosApuracaoMit")

                print(f"Situação: {situacao}")
                if dados_apuracao:
                    periodo = dados_apuracao.get("PeriodoApuracao", {})
                    print(f"Período: {periodo.get('MesApuracao')}/{periodo.get('AnoApuracao')}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_consultar_apuracao())
```

### Exemplo 24: Listar Apurações (MIT)

```python
async def exemplo_listar_apuracoes():
    """Exemplo de listagem de apurações MIT."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            response = await client.consultar(
                id_sistema="MIT",
                id_servico="LISTAAPURACOES317",
                dados={
                    "mesApuracao": 1,
                    "anoApuracao": 2025,
                    "situacaoApuracao": 3  # 3 = ENCERRADA
                }
            )

            # Resposta contém lista de apurações
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                import json
                dados_dict = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta

                apuracoes = dados_dict.get("Apuracoes", [])
                print(f"Total de apurações encontradas: {len(apuracoes)}")

                for apuracao in apuracoes:
                    id_apuracao = apuracao.get("idApuracao")
                    situacao = apuracao.get("situacao")
                    valor_total = apuracao.get("valorTotalApurado")
                    print(f"ID: {id_apuracao}, Situação: {situacao}, Valor: {valor_total}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_listar_apuracoes())
```

### Exemplo 25: Consulta Pagamento por Data (PAGTOWEB)

```python
async def exemplo_consulta_pagamento_por_data():
    """Exemplo de consulta de pagamento por intervalo de data."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            response = await client.consultar(
                id_sistema="PAGTOWEB",
                id_servico="PAGAMENTOS71",
                dados={
                    "intervaloDataArrecadacao": {
                        "dataInicial": "2019-09-01",
                        "dataFinal": "2019-11-30",
                    },
                    "primeiroDaPagina": 0,
                    "tamanhoDaPagina": 100,
                }
            )

            # Resposta contém lista de pagamentos
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                import json
                pagamentos = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta
                print(f"Total de pagamentos encontrados: {len(pagamentos) if isinstance(pagamentos, list) else 'N/A'}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_consulta_pagamento_por_data())
```

### Exemplo 26: Consulta Pagamento por Código de Receita (PAGTOWEB)

```python
async def exemplo_consulta_pagamento_por_codigo():
    """Exemplo de consulta de pagamento por código de receita."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            response = await client.consultar(
                id_sistema="PAGTOWEB",
                id_servico="PAGAMENTOS71",
                dados={
                    "codigoReceitaLista": ["9999", "8888"],
                    "primeiroDaPagina": 0,
                    "tamanhoDaPagina": 100,
                }
            )

            # Resposta contém lista de pagamentos
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                import json
                pagamentos = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta
                print(f"Total de pagamentos encontrados: {len(pagamentos) if isinstance(pagamentos, list) else 'N/A'}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_consulta_pagamento_por_codigo())
```

### Exemplo 27: Conta Consulta Pagamento (PAGTOWEB)

```python
async def exemplo_conta_consulta_pagamento():
    """Exemplo de conta consulta de pagamento."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            response = await client.consultar(
                id_sistema="PAGTOWEB",
                id_servico="CONTACONSDOCARRPG73",
                dados={
                    "intervaloDataArrecadacao": {
                        "dataInicial": "2019-09-01",
                        "dataFinal": "2019-11-30",
                    }
                }
            )

            # Resposta contém contagem de pagamentos
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                import json
                resultado = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta
                print(f"Resultado da consulta: {resultado}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_conta_consulta_pagamento())
```

### Exemplo 28: Emitir Comprovante de Pagamento (PAGTOWEB)

```python
async def exemplo_emitir_comprovante_pagamento():
    """Exemplo de emissão de comprovante de pagamento."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            response = await client.emitir(
                id_sistema="PAGTOWEB",
                id_servico="COMPARRECADACAO72",
                dados={"numeroDocumento": "99999999999999999"}
            )

            # Resposta contém o comprovante de pagamento
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                import json
                comprovante = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta
                print(f"Comprovante emitido: {comprovante}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_emitir_comprovante_pagamento())
```

### Exemplo 29: Consultar Pedidos (PARCMEI-ESP)

```python
async def exemplo_consultar_pedidos_parcmeiesp():
    """Exemplo de consulta de pedidos de parcelamento."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            # Este serviço não requer dados de entrada
            response = await client.consultar(
                id_sistema="PARCMEI-ESP",
                id_servico="PEDIDOSPARC213",
                dados={}  # Dados vazios
            )

            # Resposta contém lista de pedidos
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                import json
                pedidos = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta
                print(f"Total de pedidos encontrados: {len(pedidos) if isinstance(pedidos, list) else 'N/A'}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_consultar_pedidos_parcmeiesp())
```

### Exemplo 30: Consultar Parcelamento (PARCMEI-ESP)

```python
async def exemplo_consultar_parcelamento_parcmeiesp():
    """Exemplo de consulta de parcelamento."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            response = await client.consultar(
                id_sistema="PARCMEI-ESP",
                id_servico="OBTERPARC214",
                dados={"numeroParcelamento": 9001}
            )

            # Resposta contém dados do parcelamento
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                import json
                parcelamento = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta
                print(f"Dados do parcelamento: {parcelamento}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_consultar_parcelamento_parcmeiesp())
```

### Exemplo 31: Emitir DAS (PARCMEI-ESP)

```python
async def exemplo_emitir_das_parcmeiesp():
    """Exemplo de emissão de DAS para parcelamento."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            response = await client.emitir(
                id_sistema="PARCMEI-ESP",
                id_servico="GERARDAS211",
                dados={"parcelaParaEmitir": 202107}  # Formato YYYYMM
            )

            # Resposta contém o DAS emitido
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                import json
                das = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta
                print(f"DAS emitido: {das}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_emitir_das_parcmeiesp())
```

### Exemplo 32: Consultar Pedidos (PARCMEI)

```python
async def exemplo_consultar_pedidos_parcmei():
    """Exemplo de consulta de pedidos de parcelamento."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            # Este serviço não requer dados de entrada
            response = await client.consultar(
                id_sistema="PARCMEI",
                id_servico="PEDIDOSPARC203",
                dados={}  # Dados vazios
            )

            # Resposta contém lista de pedidos
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                import json
                pedidos = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta
                print(f"Total de pedidos encontrados: {len(pedidos) if isinstance(pedidos, list) else 'N/A'}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_consultar_pedidos_parcmei())
```

### Exemplo 33: Consultar Parcelamento (PARCMEI)

```python
async def exemplo_consultar_parcelamento_parcmei():
    """Exemplo de consulta de parcelamento."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            response = await client.consultar(
                id_sistema="PARCMEI",
                id_servico="OBTERPARC204",
                dados={"numeroParcelamento": 1}
            )

            # Resposta contém dados do parcelamento
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                import json
                parcelamento = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta
                print(f"Dados do parcelamento: {parcelamento}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_consultar_parcelamento_parcmei())
```

### Exemplo 34: Emitir DAS (PARCMEI)

```python
async def exemplo_emitir_das_parcmei():
    """Exemplo de emissão de DAS para parcelamento."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            response = await client.emitir(
                id_sistema="PARCMEI",
                id_servico="GERARDAS201",
                dados={"parcelaParaEmitir": 202107}  # Formato YYYYMM
            )

            # Resposta contém o DAS emitido
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                import json
                das = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta
                print(f"DAS emitido: {das}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_emitir_das_parcmei())
```

### Exemplo 35: Consultar Pedidos (PARCSN-ESP)

```python
async def exemplo_consultar_pedidos_parcsnesp():
    """Exemplo de consulta de pedidos de parcelamento."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            # Este serviço não requer dados de entrada
            response = await client.consultar(
                id_sistema="PARCSN-ESP",
                id_servico="PEDIDOSPARC173",
                dados={}  # Dados vazios
            )

            # Resposta contém lista de pedidos
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                import json
                pedidos = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta
                print(f"Total de pedidos encontrados: {len(pedidos) if isinstance(pedidos, list) else 'N/A'}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_consultar_pedidos_parcsnesp())
```

### Exemplo 36: Consultar Parcelamento (PARCSN-ESP)

```python
async def exemplo_consultar_parcelamento_parcsnesp():
    """Exemplo de consulta de parcelamento."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            response = await client.consultar(
                id_sistema="PARCSN-ESP",
                id_servico="OBTERPARC174",
                dados={"numeroParcelamento": 9001}
            )

            # Resposta contém dados do parcelamento
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                import json
                parcelamento = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta
                print(f"Dados do parcelamento: {parcelamento}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_consultar_parcelamento_parcsnesp())
```

### Exemplo 37: Emitir DAS (PARCSN-ESP)

```python
async def exemplo_emitir_das_parcsnesp():
    """Exemplo de emissão de DAS para parcelamento."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            response = await client.emitir(
                id_sistema="PARCSN-ESP",
                id_servico="GERARDAS171",
                dados={"parcelaParaEmitir": 202306}  # Formato YYYYMM
            )

            # Resposta contém o DAS emitido
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                import json
                das = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta
                print(f"DAS emitido: {das}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_emitir_das_parcsnesp())
```

### Exemplo 38: Consultar Pedidos (PARCSN)

```python
async def exemplo_consultar_pedidos_parcsn():
    """Exemplo de consulta de pedidos de parcelamento."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            # Este serviço não requer dados de entrada
            response = await client.consultar(
                id_sistema="PARCSN",
                id_servico="PEDIDOSPARC163",
                dados={}  # Dados vazios
            )

            # Resposta contém lista de pedidos
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                import json
                pedidos = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta
                print(f"Total de pedidos encontrados: {len(pedidos) if isinstance(pedidos, list) else 'N/A'}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_consultar_pedidos_parcsn())
```

### Exemplo 39: Consultar Parcelamento (PARCSN)

```python
async def exemplo_consultar_parcelamento_parcsn():
    """Exemplo de consulta de parcelamento."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            response = await client.consultar(
                id_sistema="PARCSN",
                id_servico="OBTERPARC164",
                dados={"numeroParcelamento": 1}
            )

            # Resposta contém dados do parcelamento
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                import json
                parcelamento = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta
                print(f"Dados do parcelamento: {parcelamento}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_consultar_parcelamento_parcsn())
```

### Exemplo 40: Emitir DAS (PARCSN)

```python
async def exemplo_emitir_das_parcsn():
    """Exemplo de emissão de DAS para parcelamento."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            response = await client.emitir(
                id_sistema="PARCSN",
                id_servico="GERARDAS161",
                dados={"parcelaParaEmitir": 202306}  # Formato YYYYMM
            )

            # Resposta contém o DAS emitido
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                import json
                das = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta
                print(f"DAS emitido: {das}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_emitir_das_parcsn())
```

### Exemplo 41: Consultar Pedidos (PERTMEI)

```python
async def exemplo_consultar_pedidos_pertmei():
    """Exemplo de consulta de pedidos de parcelamento."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            # Este serviço não requer dados de entrada
            response = await client.consultar(
                id_sistema="PERTMEI",
                id_servico="PEDIDOSPARC223",
                dados={}  # Dados vazios
            )

            # Resposta contém lista de pedidos
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                import json
                pedidos = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta
                print(f"Total de pedidos encontrados: {len(pedidos) if isinstance(pedidos, list) else 'N/A'}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_consultar_pedidos_pertmei())
```

### Exemplo 42: Consultar Parcelamento (PERTMEI)

```python
async def exemplo_consultar_parcelamento_pertmei():
    """Exemplo de consulta de parcelamento."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            response = await client.consultar(
                id_sistema="PERTMEI",
                id_servico="OBTERPARC224",
                dados={"numeroParcelamento": 9001}
            )

            # Resposta contém dados do parcelamento
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                import json
                parcelamento = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta
                print(f"Dados do parcelamento: {parcelamento}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_consultar_parcelamento_pertmei())
```

### Exemplo 43: Emitir DAS (PERTMEI)

```python
async def exemplo_emitir_das_pertmei():
    """Exemplo de emissão de DAS para parcelamento."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            response = await client.emitir(
                id_sistema="PERTMEI",
                id_servico="GERARDAS221",
                dados={"parcelaParaEmitir": 202306}  # Formato YYYYMM
            )

            # Resposta contém o DAS emitido
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                import json
                das = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta
                print(f"DAS emitido: {das}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_emitir_das_pertmei())
```

### Exemplo 44: Consultar Pedidos (PERTSN)

```python
async def exemplo_consultar_pedidos_pertsn():
    """Exemplo de consulta de pedidos de parcelamento."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            # Este serviço não requer dados de entrada
            response = await client.consultar(
                id_sistema="PERTSN",
                id_servico="PEDIDOSPARC183",
                dados={}  # Dados vazios
            )

            # Resposta contém lista de pedidos
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                import json
                pedidos = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta
                print(f"Total de pedidos encontrados: {len(pedidos) if isinstance(pedidos, list) else 'N/A'}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_consultar_pedidos_pertsn())
```

### Exemplo 45: Consultar Parcelamento (PERTSN)

```python
async def exemplo_consultar_parcelamento_pertsn():
    """Exemplo de consulta de parcelamento."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            response = await client.consultar(
                id_sistema="PERTSN",
                id_servico="OBTERPARC184",
                dados={"numeroParcelamento": 9102}
            )

            # Resposta contém dados do parcelamento
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                import json
                parcelamento = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta
                print(f"Dados do parcelamento: {parcelamento}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_consultar_parcelamento_pertsn())
```

### Exemplo 46: Emitir DAS (PERTSN)

```python
async def exemplo_emitir_das_pertsn():
    """Exemplo de emissão de DAS para parcelamento."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            response = await client.emitir(
                id_sistema="PERTSN",
                id_servico="GERARDAS181",
                dados={"parcelaParaEmitir": 202301}  # Formato YYYYMM
            )

            # Resposta contém o DAS emitido
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                import json
                das = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta
                print(f"DAS emitido: {das}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_emitir_das_pertsn())
```

### Exemplo 47: Consultar Declarações (PGDAS-D)

```python
async def exemplo_consultar_declaracoes_pgdasd():
    """Exemplo de consulta de declarações transmitidas."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            response = await client.consultar(
                id_sistema="PGDASD",
                id_servico="CONSDECLARACAO13",
                dados={"anoCalendario": "2018"}  # Formato YYYY
            )

            # Resposta contém lista de declarações
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                import json
                declaracoes = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta
                print(f"Declarações encontradas: {declaracoes}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_consultar_declaracoes_pgdasd())
```

### Exemplo 48: Gerar DAS (PGDAS-D)

```python
async def exemplo_gerar_das_pgdasd():
    """Exemplo de geração de DAS."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            response = await client.emitir(
                id_sistema="PGDASD",
                id_servico="GERARDAS12",
                dados={"periodoApuracao": "201801"}  # Formato YYYYMM
            )

            # Resposta contém o DAS gerado
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                import json
                das = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta
                print(f"DAS gerado: {das}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_gerar_das_pgdasd())
```

### Exemplo 49: Entregar Declaração (PGDAS-D)

```python
async def exemplo_entregar_declaracao_pgdasd():
    """Exemplo de entrega de declaração."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            # Estrutura complexa de declaração
            dados = {
                "cnpjCompleto": "00000000000100",
                "pa": 202101,
                "indicadorTransmissao": True,
                "indicadorComparacao": True,
                "declaracao": {
                    "tipoDeclaracao": 1,
                    "receitaPaCompetenciaInterno": 10000.00,
                    # ... outros campos da declaração
                },
            }

            response = await client.declarar(
                id_sistema="PGDASD",
                id_servico="TRANSDECLARACAO11",
                dados=dados
            )

            # Resposta contém resultado da transmissão
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                import json
                resultado = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta
                print(f"Resultado da transmissão: {resultado}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_entregar_declaracao_pgdasd())
```

### Exemplo 50: Gerar DAS (PGMEI)

```python
async def exemplo_gerar_das_pgmei():
    """Exemplo de geração de DAS."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            response = await client.emitir(
                id_sistema="PGMEI",
                id_servico="GERARDASPDF21",
                dados={"periodoApuracao": "201901"}  # Formato YYYYMM
            )

            # Resposta contém o DAS gerado
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                import json
                das = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta
                print(f"DAS gerado: {das}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_gerar_das_pgmei())
```

### Exemplo 51: Consultar Dívida Ativa (PGMEI)

```python
async def exemplo_consultar_divida_ativa_pgmei():
    """Exemplo de consulta de dívida ativa."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            response = await client.consultar(
                id_sistema="PGMEI",
                id_servico="DIVIDAATIVA24",
                dados={"anoCalendario": "2020"}  # Formato YYYY
            )

            # Resposta contém informações sobre dívida ativa
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                import json
                divida = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta
                print(f"Dívida ativa: {divida}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_consultar_divida_ativa_pgmei())
```

### Exemplo 52: Obter Procurações (PROCURACOES)

```python
async def exemplo_obter_procuracoes():
    """Exemplo de obtenção de procurações."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            response = await client.consultar(
                id_sistema="PROCURACOES",
                id_servico="OBTERPROCURACAO41",
                dados={
                    "outorgante": "99999999999999",  # CNPJ do outorgante
                    "tipoOutorgante": "2",  # "1" para CPF, "2" para CNPJ
                    "outorgado": "99999999999",  # CPF do outorgado
                    "tipoOutorgado": "1",  # "1" para CPF, "2" para CNPJ
                }
            )

            # Resposta contém informações sobre as procurações
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                import json
                procuracoes = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta
                print(f"Procurações encontradas: {procuracoes}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_obter_procuracoes())
```

### Exemplo 53: Efetuar Opção de Regime (REGIME APURACAO)

```python
async def exemplo_efetuar_opcao_regime():
    """Exemplo de efetuação de opção de regime."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            response = await client.declarar(
                id_sistema="REGIMEAPURACAO",
                id_servico="EFETUAROPCAOREGIME101",
                dados={
                    "anoOpcao": 2023,
                    "tipoRegime": 1,
                    "descritivoRegime": "CAIXA",
                    "deAcordoResolucao": True,
                }
            )

            # Resposta contém resultado da opção
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                import json
                resultado = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta
                print(f"Resultado da opção: {resultado}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_efetuar_opcao_regime())
```

### Exemplo 54: Consultar Opção de Regime (REGIME APURACAO)

```python
async def exemplo_consultar_opcao_regime():
    """Exemplo de consulta de opção de regime."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            response = await client.consultar(
                id_sistema="REGIMEAPURACAO",
                id_servico="CONSULTAROPCAOREGIME103",
                dados={"anoCalendario": 2023}
            )

            # Resposta contém informações sobre a opção de regime
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                import json
                opcao = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta
                print(f"Opção de regime: {opcao}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_consultar_opcao_regime())
```

### Exemplo 55: Consultar Pedidos (RELPMEI)

```python
async def exemplo_consultar_pedidos_relpmei():
    """Exemplo de consulta de pedidos de parcelamento."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            # Este serviço não requer dados de entrada
            response = await client.consultar(
                id_sistema="RELPMEI",
                id_servico="PEDIDOSPARC233",
                dados={}  # Dados vazios
            )

            # Resposta contém lista de pedidos
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                import json
                pedidos = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta
                print(f"Total de pedidos encontrados: {len(pedidos) if isinstance(pedidos, list) else 'N/A'}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_consultar_pedidos_relpmei())
```

### Exemplo 56: Emitir DAS (RELPMEI)

```python
async def exemplo_emitir_das_relpmei():
    """Exemplo de emissão de DAS para parcelamento."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            response = await client.emitir(
                id_sistema="RELPMEI",
                id_servico="GERARDAS231",
                dados={"parcelaParaEmitir": 202304}  # Formato YYYYMM
            )

            # Resposta contém o DAS emitido
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                import json
                das = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta
                print(f"DAS emitido: {das}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_emitir_das_relpmei())
```

### Exemplo 57: Consultar Pedidos (RELPSN)

```python
async def exemplo_consultar_pedidos_relpsn():
    """Exemplo de consulta de pedidos de parcelamento."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            # Este serviço não requer dados de entrada
            response = await client.consultar(
                id_sistema="RELPSN",
                id_servico="PEDIDOSPARC193",
                dados={}  # Dados vazios
            )

            # Resposta contém lista de pedidos
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                import json
                pedidos = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta
                print(f"Total de pedidos encontrados: {len(pedidos) if isinstance(pedidos, list) else 'N/A'}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_consultar_pedidos_relpsn())
```

### Exemplo 58: Emitir DAS (RELPSN)

```python
async def exemplo_emitir_das_relpsn():
    """Exemplo de emissão de DAS para parcelamento."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            response = await client.emitir(
                id_sistema="RELPSN",
                id_servico="GERARDAS191",
                dados={"parcelaParaEmitir": 202308}  # Formato YYYYMM
            )

            # Resposta contém o DAS emitido
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                import json
                das = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta
                print(f"DAS emitido: {das}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_emitir_das_relpsn())
```

### Exemplo 59: Gerar DARF Consolidado (SICALC)

```python
async def exemplo_gerar_darf_consolidado():
    """Exemplo de geração de DARF consolidado."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            response = await client.emitir(
                id_sistema="SICALC",
                id_servico="CONSOLIDARGERARDARF51",
                dados={
                    "uf": "SP",
                    "municipio": "7107",
                    "codigoReceita": "0190",
                    "codigoReceitaExtensao": "01",
                    "tipoPA": "ME",
                    "dataPA": "12/2017",
                    "vencimento": "2018-01-31T00:00:00",
                    "valorImposto": "1000.00",
                    "dataConsolidacao": "2022-08-08T00:00:00",
                    "observacao": "Darf calculado",
                }
            )

            # Resposta contém o DARF gerado
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                import json
                darf = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta
                print(f"DARF gerado: {darf}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_gerar_darf_consolidado())
```

### Exemplo 60: Consultar Receitas do SICALC

```python
async def exemplo_consultar_receitas_sicalc():
    """Exemplo de consulta de receitas do SICALC."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            response = await client.apoiar(
                id_sistema="SICALC",
                id_servico="CONSULTAAPOIORECEITAS52",
                dados={"codigoReceita": "6106"}
            )

            # Resposta contém informações sobre a receita
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                import json
                receita = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta
                print(f"Informações da receita: {receita}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_consultar_receitas_sicalc())
```

### Exemplo 61: Solicitar Protocolo do Relatório de Situação Fiscal (SITFIS)

```python
async def exemplo_solicitar_protocolo_sitfis():
    """Exemplo de solicitação de protocolo do relatório de situação fiscal."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            # Este serviço não requer dados de entrada
            response = await client.apoiar(
                id_sistema="SITFIS",
                id_servico="SOLICITARPROTOCOLO91",
                dados={}  # Dados vazios
            )

            # Resposta contém o protocolo
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                import json
                protocolo = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta
                print(f"Protocolo obtido: {protocolo}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_solicitar_protocolo_sitfis())
```

### Exemplo 62: Emitir Relatório de Situação Fiscal (SITFIS)

```python
async def exemplo_emitir_relatorio_sitfis():
    """Exemplo de emissão de relatório de situação fiscal."""
    from integra_sdk import IntegraClient

    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            # Primeiro, solicitar o protocolo
            protocolo_response = await client.apoiar(
                id_sistema="SITFIS",
                id_servico="SOLICITARPROTOCOLO91",
                dados={}
            )

            # Extrair o protocolo da resposta
            protocolo_dados = protocolo_response.get("dados", {})
            if isinstance(protocolo_dados, str):
                import json
                protocolo_dados = json.loads(protocolo_dados)

            protocolo = protocolo_dados.get("protocoloRelatorio", "")

            # Emitir o relatório usando o protocolo
            response = await client.emitir(
                id_sistema="SITFIS",
                id_servico="RELATORIOSITFIS92",
                dados={"protocoloRelatorio": protocolo}
            )

            # Resposta contém o relatório
            dados_resposta = response.get("dados", {})
            if dados_resposta:
                import json
                relatorio = json.loads(dados_resposta) if isinstance(dados_resposta, str) else dados_resposta
                print(f"Relatório emitido: {relatorio}")

        except ValidationError as e:
            print(f"Dados inválidos: {e.errors()}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_emitir_relatorio_sitfis())
```

### Exemplo 3: Enviar XML Assinado (AUTENTICAPROCURADOR)

```python
import base64

async def exemplo_apoiar():
    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            # XML deve estar codificado em Base64
            xml_content = """<termoDeAutorizacao>
                <dados>
                    <sistema id="API Integra Contador" />
                    <termo texto="Autorizo..." />
                </dados>
            </termoDeAutorizacao>"""
            xml_base64 = base64.b64encode(xml_content.encode("utf-8")).decode("utf-8")

            response = await client.apoiar(
                id_sistema="AUTENTICAPROCURADOR",
                id_servico="ENVIOXMLASSINADO81",
                dados={"xml": xml_base64}
            )

            # Resposta contém token do procurador e data de expiração
            # Os dados são retornados no formato original da API (camelCase)
            dados = response.get("dados", {})
            if dados:
                print(f"Token: {dados.get('autenticar_procurador_token')}")
                print(f"Expira em: {dados.get('data_hora_expiracao')}")
        except ValidationError as e:
            print(f"Dados inválidos: {e.errors}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_apoiar())
```

### Exemplo 4: Obter Indicador de Novas Mensagens (CAIXAPOSTAL)

```python
async def exemplo_monitorar():
    # Em Trial, token é opcional
    async with IntegraClient("Trial", config) as client:
        try:
            # Este serviço não requer dados de entrada
            response = await client.monitorar(
                id_sistema="CAIXAPOSTAL",
                id_servico="INNOVAMSG63",
                dados={}  # Dados vazios - este serviço não requer parâmetros
            )

            # Resposta contém indicador de novas mensagens
            # Os dados são retornados no formato original da API (camelCase)
            dados = response.get("dados", {})
            if dados:
                # Acesse os campos no formato original da API
                conteudo = dados.get("conteudo", [])
                if conteudo and len(conteudo) > 0:
                    indicador = conteudo[0].get("indicadorMensagensNovas")
                    print(f"Indicador de novas mensagens: {indicador}")
                    if indicador and indicador != "0":
                        print("Há novas mensagens!")
                    else:
                        print("Não há novas mensagens.")
        except ValidationError as e:
            print(f"Dados inválidos: {e.errors}")
        except APIError as e:
            print(f"Erro da API: {e.status_code} - {e}")

asyncio.run(exemplo_monitorar())
```

## Formato de Resposta

**Importante**: O SDK retorna os dados **exatamente como a API fornece**, sem transformações ou parsing customizado. Isso significa:

- **Nomes de campos preservados**: Os campos mantêm seus nomes originais (camelCase, etc.)
- **Estrutura original**: A estrutura dos dados é a mesma retornada pela API
- **Apenas parse básico**: O único processamento é converter o campo `dados` de string JSON para objeto/dict quando necessário

**Exemplo de resposta**:

```python
{
    "status": 200,
    "mensagens": [...],
    "contratante": {...},
    "contribuinte": {...},
    "dados": {
        "codigo": "00",
        "conteudo": [
            {
                "codigoSistemaRemetente": "00014",  # camelCase original
                "assuntoModelo": "Assunto",
                "dataEnvio": "20220620",
                # ... outros campos no formato original
            }
        ]
    }
}
```

## Métodos Disponíveis

O cliente suporta os seguintes métodos HTTP da API:

| Método SDK     | Endpoint API        | Descrição              |
| -------------- | ------------------- | ---------------------- |
| `consultar()`  | POST /v1/Consultar  | Consultar informações  |
| `emitir()`     | POST /v1/Emitir     | Emitir documentos      |
| `transmitir()` | POST /v1/Transmitir | Transmitir declarações |
| `declarar()`   | POST /v1/Declarar   | Entregar declarações   |
| `apoiar()`     | POST /v1/Apoiar     | Apoiar processos       |
| `monitorar()`  | POST /v1/Monitorar  | Monitorar eventos      |

## Templates Disponíveis

### AUTENTICAPROCURADOR

- **ENVIOXMLASSINADO81**: Envio de XML assinado com o Termo de Autorização

### CAIXAPOSTAL

- **MSGCONTRIBUINTE61**: Obter Lista de Mensagens por Contribuintes
- **MSGDETALHAMENTO62**: Obter Detalhes de uma Mensagem Específica
- **INNOVAMSG63**: Obter Indicador de Novas Mensagens

### CCMEI

- **CCMEISITCADASTRAL123**: Consulta a situação cadastral dos CNPJ MEI vinculados ao CPF
- **DADOSCCMEI122**: Consulta os dados do Certificado de Condição MEI
- **EMITIRCCMEI121**: Emissão do Certificado de Condição de MEI em formato PDF

### DCTFWEB

- **GERARGUIA31**: Gerar Documento de Arrecadação
- **GERARGUIAANDAMENTO313**: Gerar Guia em Andamento
- **CONSXMLDECLARACAO38**: Consultar XML da Declaração
- **CONSRECIBO32**: Consultar Recibo de Transmissão
- **CONSDECCOMPLETA33**: Consultar Relatório Declaração Completa
- **TRANSDECLARACAO310**: Transmitir Declaração

### DEFIS

- **TRANSDECLARACAO141**: Entregar Defis
- **CONSDECLARACAO142**: Consultar Declarações
- **CONSULTIMADECREC143**: Consultar Última Declaração e Recibo
- **CONSDECREC144**: Consultar Declaração e Recibo

### DTE

- **CONSULTASITUACAODTE111**: Obter indicador DTE

### E-PROCESSO

- **CONSPROCPORINTER271**: Consultar Processos por Interessado

### EVENTOS ATUALIZACAO

- **SOLICEVENTOSPF131**: Solicitar eventos de PF
- **OBTEREVENTOSPF133**: Obter eventos de PF
- **SOLICEVENTOSPJ132**: Solicitar eventos de PJ
- **OBTEREVENTOSPJ134**: Obter eventos de PJ

### MIT

- **ENCAPURACAO314**: Encerrar Apuração
- **SITUACAOENC315**: Consulta a situação do encerramento
- **CONSAPURACAO316**: Consultar Apuração
- **LISTAAPURACOES317**: Listar Apuração por mês e ano

### PAGTOWEB

- **PAGAMENTOS71**: Consulta Pagamento (por intervaloDataArrecadacao, codigoReceitaLista, ou intervaloValorTotalDocumento)
- **COMPARRECADACAO72**: Emitir Comprovante de Pagamento
- **CONTACONSDOCARRPG73**: Conta Consulta Pagamento (por intervaloDataArrecadacao, codigoReceitaLista, ou intervaloValorTotalDocumento)

### PARCMEI-ESP

- **PEDIDOSPARC213**: Consultar pedidos
- **OBTERPARC214**: Consultar Parcelamento
- **PARCELASPARAGERAR212**: Consultar Parcelas para Impressão
- **DETPAGTOPARC215**: Consultar Detalhes de Pagamento
- **GERARDAS211**: Emitir DAS

### PARCMEI

- **PEDIDOSPARC203**: Consultar pedidos
- **OBTERPARC204**: Consultar Parcelamento
- **PARCELASPARAGERAR202**: Consultar Parcelas para Impressão
- **DETPAGTOPARC205**: Consultar Detalhes de Pagamento
- **GERARDAS201**: Emitir DAS

### PARCSN-ESP

- **PEDIDOSPARC173**: Consultar pedidos
- **OBTERPARC174**: Consultar Parcelamento
- **PARCELASPARAGERAR172**: Consultar Parcelas para Impressão
- **DETPAGTOPARC175**: Consultar Detalhes de Pagamento
- **GERARDAS171**: Emitir DAS

### PARCSN

- **PEDIDOSPARC163**: Consultar pedidos
- **OBTERPARC164**: Consultar Parcelamento
- **PARCELASPARAGERAR162**: Consultar Parcelas para Impressão
- **DETPAGTOPARC165**: Consultar Detalhes de Pagamento
- **GERARDAS161**: Emitir DAS

### PERTMEI

- **PEDIDOSPARC223**: Consultar pedidos
- **OBTERPARC224**: Consultar Parcelamento
- **PARCELASPARAGERAR222**: Consultar Parcelas para Impressão
- **DETPAGTOPARC225**: Consultar Detalhes de Pagamento
- **GERARDAS221**: Emitir DAS

### PERTSN

- **PEDIDOSPARC183**: Consultar pedidos
- **OBTERPARC184**: Consultar Parcelamento
- **PARCELASPARAGERAR182**: Consultar Parcelas para Impressão
- **DETPAGTOPARC185**: Consultar Detalhes de Pagamento
- **GERARDAS181**: Emitir DAS

### PGDAS-D

- **CONSDECLARACAO13**: Consultar Declarações Transmitidas por Ano-Calendário ou Período de Apuração
- **GERARDAS12**: Gerar DAS
- **CONSULTIMADECREC14**: Consultar a Última Declaração/Recibo
- **CONSDECREC15**: Consultar Declaração/Recibo
- **CONSEXTRATO16**: Consultar Extrato do DAS
- **TRANSDECLARACAO11**: Entregar Declaração
- **GERARDASAVULSO19**: Gerar DAS Avulso
- **GERARDASCOBRANCA17**: Gerar DAS Cobrança
- **GERARDASPROCESSO18**: Gerar DAS de Processo

### PGMEI

- **GERARDASPDF21**: Gerar DAS
- **GERARDASCODBARRA22**: Gerar DAS Código de Barras
- **ATUBENEFICIO23**: Atualizar Benefício
- **DIVIDAATIVA24**: Consultar Dívida Ativa

### PROCURACOES

- **OBTERPROCURACAO41**: Obter Procurações

### REGIME APURACAO

- **EFETUAROPCAOREGIME101**: Efetuar opção
- **CONSULTARANOSCALENDARIOS102**: Consultar Anos Calendários
- **CONSULTAROPCAOREGIME103**: Consultar opção Regime
- **CONSULTARRESOLUCAO104**: Consultar Resolução

### RELPMEI

- **PEDIDOSPARC233**: Consultar pedidos
- **OBTERPARC234**: Consultar Parcelamento
- **PARCELASPARAGERAR232**: Consultar Parcelas para Impressão
- **DETPAGTOPARC235**: Consultar Detalhes de Pagamento
- **GERARDAS231**: Emitir DAS

### RELPSN

- **PEDIDOSPARC193**: Consultar pedidos
- **OBTERPARC174**: Consultar Parcelamento
- **PARCELASPARAGERAR192**: Consultar Parcelas para Impressão
- **DETPAGTOPARC195**: Consultar Detalhes de Pagamento
- **GERARDAS191**: Emitir DAS

### SICALC

- **CONSOLIDARGERARDARF51**: Gerar DARF consolidado (Pessoa Física, Pessoa Jurídica com cotas, etc.)
- **GERARDARFCODBARRA53**: Gerar DARF com código de barras
- **CONSULTAAPOIORECEITAS52**: Consultar Receitas do SICALC

### SITFIS

- **SOLICITARPROTOCOLO91**: Solicitar protocolo do relatório de situação fiscal
- **RELATORIOSITFIS92**: Emitir Relatório de Situação Fiscal

## Autenticação

O SDK suporta dois métodos de autenticação:

1. **Token Bearer estático**: Fornece um token diretamente (modo atual)
2. **Credenciais OAuth**: Fornece `consumer_key` e `consumer_secret` para obtenção automática de tokens

### Método 1: Token Bearer Estático

#### Comportamento por Ambiente

| Ambiente     | Token       | Comportamento                                                                              |
| ------------ | ----------- | ------------------------------------------------------------------------------------------ |
| **Trial**    | Opcional    | Se não fornecido, usa automaticamente o token fixo: `06aef429-a981-3ec5-a1f8-71d38d86481e` |
| **Trial**    | Fornecido   | Usa o token fornecido                                                                      |
| **Produção** | Obrigatório | Deve ser fornecido sempre, caso contrário lança `ValueError`                               |

#### Exemplos

```python
# ✅ Trial sem token (usa token fixo)
client = IntegraClient("Trial", config)

# ✅ Trial com token customizado
client = IntegraClient("Trial", config, token="token-customizado")

# ✅ Produção com token
client = IntegraClient("Production", config, token="token-producao")

# ❌ Produção sem token (lança ValueError)
client = IntegraClient("Production", config)  # Erro!
```

### Método 2: Autenticação com Certificado Digital (Obrigatório para Produção)

O SDK pode gerenciar automaticamente a obtenção e renovação de tokens usando autenticação com certificado digital. **O certificado é OBRIGATÓRIO** para autenticação - não há autenticação sem certificado.

#### Características

- **Cache automático**: Tokens são armazenados em cache e reutilizados até expirarem
- **Renovação automática**: Quando o token expira, um novo é obtido automaticamente
- **Certificado obrigatório**: O certificado digital (.p12) é obrigatório para autenticação
- **JWT Token automático**: Em produção, o `jwt_token` é automaticamente incluído nas requisições

#### Como Funciona

1. **Autenticação**: Usa `consumer_key`, `consumer_secret` e certificado digital para obter tokens
2. **Tokens obtidos**: Retorna `access_token` e `jwt_token`
3. **Requisições**:
   - Header `Authorization: Bearer {access_token}`
   - Header `jwt_token: {jwt_token}` (adicionado automaticamente em produção)

#### Uso com Certificado Digital

```python
from integra_sdk import IntegraClient

config = {
    "contratante": {"numero": "12345678000190", "tipo": 2},
    "contribuinte": {"numero": "12345678000190", "tipo": 2},
    "autorPedidoDados": {"numero": "12345678000190", "tipo": 2}
}

# Certificado é OBRIGATÓRIO - todos os parâmetros devem ser fornecidos
client = IntegraClient(
    "Production",
    config,
    consumer_key="sua-consumer-key",
    consumer_secret="sua-consumer-secret",
    certificate_path="/caminho/para/certificado.p12",
    certificate_password="senha-do-certificado"
)

# O token será obtido automaticamente antes de cada requisição
# O jwt_token será incluído automaticamente em requisições de produção
async with client:
    response = await client.consultar("CAIXAPOSTAL", "MSGDETALHAMENTO62", {"isn": "123"})
```

**Importante**: Em produção, todas as requisições precisam do header `jwt_token`. O SDK adiciona isso automaticamente quando você usa autenticação com certificado.

#### Obter Token Manualmente

Se necessário, você pode obter o token manualmente:

```python
async with client:
    token_info = await client.authenticate()
    print(f"Access Token: {token_info['access_token']}")
    print(f"JWT Token: {token_info['jwt_token']}")
    print(f"Expires in: {token_info['expires_in']} seconds")
```

#### Usando AuthManager Diretamente

Para uso avançado, você pode usar o `AuthManager` diretamente:

```python
from integra_sdk.auth import AuthManager
import httpx

# Criar manager
auth_manager = AuthManager(
    consumer_key="sua-key",
    consumer_secret="sua-secret",
    certificate_path="/caminho/cert.p12",  # Opcional
    certificate_password="senha"  # Opcional
)

# Obter token
async with httpx.AsyncClient() as session:
    token_response = await auth_manager.get_token(session)
    print(f"Token: {token_response.access_token}")

# Limpar cache (forçar nova obtenção)
auth_manager.clear_cache()
```

### Tratamento de Erros de Autenticação

O SDK fornece exceções específicas para erros de autenticação:

```python
from integra_sdk.exceptions import (
    InvalidCredentialsError,
    CertificateError,
    AuthError
)

try:
    client = IntegraClient("Production", config, consumer_key="key", consumer_secret="secret")
    # ...
except InvalidCredentialsError as e:
    print(f"Credenciais inválidas: {e}")
except CertificateError as e:
    print(f"Erro com certificado: {e}")
except AuthError as e:
    print(f"Erro de autenticação: {e}")
```

## Tratamento de Erros

O SDK define as seguintes exceções:

- `IntegraSDKError`: Exceção base para todos os erros do SDK
- `RequestNotFoundError`: Template não encontrado para o sistema/serviço
- `ValidationError`: Dados de entrada inválidos
- `HTTPError`: Erro HTTP (timeout, conexão, etc.)
- `APIError`: Erro retornado pela API (4xx, 5xx)
- `AuthError`: Exceção base para erros de autenticação
- `InvalidCredentialsError`: Credenciais inválidas (401, 403)
- `CertificateError`: Erro com certificado digital (400)
- `TokenExpiredError`: Token expirado (geralmente tratado automaticamente)

```python
from integra_sdk.exceptions import (
    RequestNotFoundError,
    ValidationError,
    APIError,
    HTTPError
)

try:
    response = await client.consultar(...)
except RequestNotFoundError:
    # Template não existe
    pass
except ValidationError as e:
    # Dados inválidos - e.errors contém detalhes
    print(e.errors)
except APIError as e:
    # Erro da API - e.status_code e e.response_body disponíveis
    print(f"Status: {e.status_code}")
except HTTPError as e:
    # Erro de rede/timeout
    print(f"Erro HTTP: {e}")
```

## Estrutura do Projeto

```
integra_sdk/
├── src/
│   └── integra_sdk/
│       ├── client.py              # Cliente principal
│       ├── config.py              # Configuração
│       ├── http/                  # Camada HTTP
│       ├── templates/             # Templates de requisição
│       ├── loader/                # Carregamento de templates
│       ├── builder/               # Construção de requisições
│       ├── exceptions/            # Exceções customizadas
│       ├── types/                 # Models Pydantic
│       └── utils/                 # Utilitários
└── tests/                         # Testes
```

## Desenvolvimento

### Adicionar um Novo Template

1. Crie um novo arquivo em `templates/[sistema]/[acao].py`
2. Herde de `BaseTemplate` e implemente os métodos:
   - `validate()`: Validação dos dados
   - `get_endpoint()`: Nome do endpoint da API
3. Registre o template:

```python
from integra_sdk.templates.base import BaseTemplate
from integra_sdk.templates.registry import TemplateRegistry

class MeuTemplate(BaseTemplate):
    def __init__(self):
        super().__init__("SISTEMA", "SERVICO", "1.0")

    def validate(self, dados):
        # Validação aqui
        return dados

    def get_endpoint(self):
        return "Consultar"

# Registrar
TemplateRegistry.register("SISTEMA", "SERVICO", MeuTemplate)
```

## Requisitos

- Python 3.9+
- pydantic>=2.0.0
- httpx>=0.25.0
- typing-extensions>=4.5.0

## Licença

Este projeto está licenciado sob a [Apache License 2.0](LICENSE).
