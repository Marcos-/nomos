import scrapy

class Spider(scrapy.Spider):
    name = 'stjspider'
    start_urls = ['https://ww2.stj.jus.br/processo/pesquisa/?termo=&aplicacao=processos.ea&tipoPesquisa=tipoPesquisaGenerica&chkordem=DESC&chkMorto=MORTO']

    def parse(self, response):
        self.log(response.css('title::text').extract()[0])

        data = [
            ('aplicacao', 'processos.ea'),
            ('acao', 'pushconsultarprocessoconsultalimitenaoatendidasjaincluidas'),
            ('descemail', ''),
            ('senha', ''),
            ('NumPaginaAtual', '1'),
            ('NumTotalRegistros', '36892'),
            ('VaiParaPaginaAnterior', 'false'),
            ('VaiParaPaginaSeguinte', 'true'),
            ('ComProximaPagina', 'TRUE'),
            ('totalRegistrosPorPagina', '40'),
            ('tipoPesquisaSecundaria', ''),
            ('sequenciaisParteAdvogado', '-1'),
            ('refinamentoAdvogado', ''),
            ('refinamentoParte', ''),
            ('tipoOperacaoFonetica', ''),
            ('tipoOperacaoFoneticaPhonos', '2'),
            ('origemOrgaosSelecionados', ''),
            ('origemUFSelecionados', ''),
            ('julgadorOrgaoSelecionados', ''),
            ('tipoRamosDireitoSelecionados', 'AD'),
            ('situacoesSelecionadas', ''),
            ('num_processo', ''),
            ('num_registro', ''),
            ('numeroUnico', ''),
            ('numeroOriginario', ''),
            ('advogadoCodigo', ''),
            ('dataAutuacaoInicial', ''),
            ('dataAutuacaoFinal', ''),
            ('dataPublicacaoInicial', '29/10/2017'),
            ('dataPublicacaoFinal', '29/07/2017'),
            ('parteAutor', 'FALSE'),
            ('parteReu', 'FALSE'),
            ('parteOutros', 'FALSE'),
            ('parteNome', ''),
            ('opcoesFoneticaPhonosParte', '2'),
            ('quantidadeMinimaTermosPresentesParte', '1'),
            ('advogadoNome', ''),
            ('opcoesFoneticaPhonosAdvogado', '2'),
            ('quantidadeMinimaTermosPresentesAdvogado', '1'),
            ('conectivo', 'OU'),
            ('listarProcessosOrdemDescrecente', 'TRUE'),
            ('listarProcessosOrdemDescrecenteTemp', 'TRUE'),
            ('listarProcessosAtivosSomente', 'FALSE'),
            ('listarProcessosEletronicosSomente', 'FALSE'),
        ]


        yield scrapy.FormRequest('https://ww2.stj.jus.br/processo/pesquisa/',
                                  meta={'cookiejar': 1},
                                  formdata=dict(data),
                                  dont_filter=True,
                                  callback=self.parse_list)

    def parse_list(self, response):

        caminho_xpath = "/html/body[@id='voltarTopo']/div[@id='idInterfaceVisualCorpo']/" \
                        "div[@ id='idInterfaceVisualBlocoDeMenuBannersNavegacaoAplicacao']/" \
                        "div[@ id='idInterfaceVisualBlocoDeMenuBannersNavegacaoAplicacaoEmpacotador']/" \
                        "div[@ id='idInterfaceVisualBlocoDeMenuBannersNavegacaoAplicacaoEmpacotadorInterno']/" \
                        "div[@ id='idInterfaceVisualAreaAreaTitulo']/div[@ id='idInterfaceVisualAreaBlocoExterno']/" \
                        "div[@ id='idInterfaceVisualArea']/div[@ id='idInterfaceVisualAreaBlocoInterno']/" \
                        "span[@ id='idSpanConteudoCentro']/div[@ id='idBlocoLinhasProcesso']/" \
                        "div[@ id='idBlocoInternoLinhasProcesso']/" \
                        "div[@class='clsListaProcessoFormatoVerticalBlocoExterno'][2]/" \
                        "span[@class='clsListaProcessoFormatoVerticalLinha clsListaProcessoFormatoVerticalBlocoEscuro']/" \
                        "span[@class='clsBlocoProcessoColuna1e2e3e4 clsBlocoProcessoUfNumeroRegistroDataAutuacaoTipo']/" \
                        "span[@class='clsBlocoProcessoColuna1e2 clsBlocoProcessoUfNumeroRegistro']/" \
                        "span[@class='clsBlocoProcessoColuna clsBlocoProcessoColuna2 classSpanNumeroRegistro']/a/@href"

        link = response.xpath(caminho_xpath).extract()[0]

        self.log("https://ww2.stj.jus.br" + link)

        yield scrapy.Request("https://ww2.stj.jus.br" + link,
                       callback=self.parse_details)

    def parse_details(self, response):

        caminho_xpath = "//span[@id='idProcessoDetalhesBloco1']"

        processo = caminho_xpath + "/div[@class='classDivLinhaDetalhes'][1]/span[@class='classSpanDetalhesTexto']"
        parte_ativa = caminho_xpath + "/div[@id='idDetalhesPartesAdvogadosProcuradores']/" \
                                      "div[@class='classDivLinhaDetalhes'][1]/span[@class='classSpanDetalhesTexto']/a"

        details = response.xpath(caminho_xpath).extract()

        self.log(details)