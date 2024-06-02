from py_rpautom.python_utils import (
    abrir_arquivo_pdf,
    cls,
    escrever_em_arquivo,
    retornar_arquivos_em_pasta,
    coletar_extensao_arquivo,
)


# LOCALIZA OS ARQUIVOS PARA PROCESSAMENTO
diretorio_raiz = r'D:\OneDrive - 5t2tj5\Documents\Idiomas\russkiy\Level 1'
lista_licoes = retornar_arquivos_em_pasta(caminho=diretorio_raiz)

# DEFINE O ARQUIVO DE RESULTADO
arquivo_resultado = r'C:\dev\projects\ExtracaoTabelaRussaL1\data\tabela_extraida.csv'

# FILTRA SOMENTE OS ARQUIVOS NECESSÁRIOS
lista_arquivos_licoes = []
for arquivo in lista_licoes:
    if '.pdf' in coletar_extensao_arquivo(caminho=arquivo):
        if not ('recordingscript' in arquivo) \
        and not ('checklist' in arquivo):
            lista_arquivos_licoes.append(arquivo)

# PARA CADA ARQUIVO LOCALIZADO...
for arquivo_licao in lista_arquivos_licoes:
    # LIMPA AS VARIÁVEIS
    conteudo_pagina_tabela = []
    conteudo_tabela = []
    validacao_breakpoint = False

    # ABRE O ARQUIVO
    conteudo = abrir_arquivo_pdf(
        arquivo_pdf = arquivo_licao
    )

    # SALVA O CAMINHO DO ARQUIVO ATUAL NO ARQUIVO DE RESULTADO
    escrever_em_arquivo(
        arquivo = arquivo_resultado,
        conteudo = f'Arquivo: {arquivo_licao}',
        encoding = 'utf8',
        modo = 'a',
        nova_linha = '\r\n'
    )

    # PARA DEBUG
    # ALTERAR O VALOR DO CONTAINS CONFORME REGRA DE PARADA
    if arquivo_licao.__contains__('\\06\\'):
        # ALTERAR VARIÁVEL ABAIXO PARA TRUE EM CASO DE DEBUG
        validacao_breakpoint = False
    
    # PARA DEBUG
    if validacao_breakpoint is True:
        breakpoint()

    # LOCALIZA A PÁGINA ONDE A TABELA ESTÁ
    numero_pagina = 1
    for pagina in conteudo:
        if True in [
            'RussianRomanizationEnglishClass' in linha.replace(' ', '')
            for linha in conteudo[numero_pagina - 1]
        ]:
            break

        numero_pagina = numero_pagina + 1

    # COLETA APENAS OS DADOS DA PÁGINA DA TABELA
    conteudo_pagina_tabela = conteudo[numero_pagina - 1]

    # PARA DEBUG
    if validacao_breakpoint is True:
        breakpoint()

    # LOCALIZA O INÍCIO E O FIM DA TABELA
    numero_linha_inicio = 1
    numero_linha_fim = 1
    validacao_inico = False
    validacao_fim = False
    for linha in conteudo_pagina_tabela:
        if 'RussianRomanizationEnglishClass' in linha.replace(' ', ''):
            validacao_inico = True

        if 'SAMPLE SENTENCES' in linha:
            validacao_fim = True

        if validacao_inico is False:
            numero_linha_inicio = numero_linha_inicio + 1

        if validacao_fim is False:
            numero_linha_fim = numero_linha_fim + 1

        if (validacao_inico is True) and (validacao_fim is True):
            break

    # CASO NÃO LOCALIZE O INÍCIO OU O FIM DA TABELA,
    #   ENCERRA O PROCESSO COM AVISO DE ERRO
    if (
        (validacao_inico is True)
        and (validacao_fim is True)
    ) is False:
        print(arquivo_licao)
        print('validacao_inico: ', (validacao_inico is True))
        print('validacao_fim: ', (validacao_fim is True))
        print('Aconteceu um erro aqui!')
        break

    # PARA DEBUG
    if validacao_breakpoint is True:
        breakpoint()

    # COLETA A TABELA INTEIRA
    for linha in conteudo_pagina_tabela[
        numero_linha_inicio:numero_linha_fim-1
    ]:
        conteudo_tabela.append(linha)

    # PARA DEBUG
    if validacao_breakpoint is True:
        breakpoint()

    # SALVA A TABELA NO ARQUIVO DE RESULTADO
    for linha in conteudo_tabela:
        escrever_em_arquivo(
            arquivo=r'C:\dev\projects\ExtracaoTabelaRussaL1\data\tabela_extraida.csv',
            conteudo=linha,
            encoding='utf8',
            modo='a',
            nova_linha='\n'
        )

    # ADICIONA UMA LINHA VAZIA NO ARQUIVO DE RESULTADO
    escrever_em_arquivo(
        arquivo=r'C:\dev\projects\ExtracaoTabelaRussaL1\data\tabela_extraida.csv',
        conteudo='',
        encoding='utf8',
        modo='a',
        nova_linha='\n'
    )
