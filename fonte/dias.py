# -*- coding: utf-8 -*-
"""O DIA A DIA do guia — escrito a mao, conferido contra os dias de fechamento.

Cada bloco cita lugares por um PEDACO DO NOME (`refs`). O `build.py` casa esse
pedaco com a pesquisa da cidade e FALHA se nao achar ou se achar mais de um —
assim um lugar renomeado na pesquisa nao some do roteiro em silencio.

Regras que moldaram a ordem (todas da pesquisa de 30/09/2026):
  - Domingo 21/02 em Roma: Vaticano, Testaccio, CasaManco, Suppli Roma,
    Roscioli, Peroni e Formula 1 fecham. Trapizzino, Emma e Da Fortunata abrem.
  - Segunda 22/02: Galleria Borghese e Castel Sant'Angelo fecham -> Roma Antiga.
  - Terca 23/02: Il Grottino fecha. Retirada dos ingressos da audiencia do Papa
    e' terca 15h-19h no Portao de Bronze -> Vaticano na terca.
  - Innsbruck: museu do Telhado de Ouro fecha segunda no inverno -> domingo.
  - Viena: Kunsthistorisches e Schnitzelwirt fecham segunda.
  - Budapeste: Sinagoga fecha sabado e fecha cedo sexta -> quinta.
  - Madri: Rastro e a Euromania do 100 Montaditos (tudo a 1 euro) so domingo
    07/03. Troca da guarda do Palacio Real quarta e sabado 11h-14h -> sab 20/02.
    Segunda 08/03 (Dia da Mulher): marchas no centro a noite -> sair 17h30.
"""

DIAS = [
  dict(data="2027-02-18", cidade="madri", titulo="Voo e chegada", noite="Madri",
    blocos=[
      ("Dia", "CA898 sai de Guarulhos às 08:25 e pousa em Madri às 22:35 (T1). Imigração com o registro biométrico novo (EES), malas, e direto para a hospedagem.", []),
      ("Do aeroporto", "<b>Táxi:</b> peçam na saída, no ponto de táxi, para quantas pessoas forem; eles mandam carro grande. <b>Uber:</b> antes de sair para a rua, subam a rampa à direita até o estacionamento, que é onde os carros de aplicativo pegam passageiros.", []),
      ("Se bater fome", "A essa hora quase tudo está fechado. O mais garantido é pedir no Uber Eats já no caminho, para chegar junto. Se a hospedagem for perto de Sol, a Chocolatería San Ginés não fecha.", ["San Ginés"]),
    ]),
  dict(data="2027-02-19", cidade="madri", titulo="Retiro, Letras e o Prado de graça", noite="Madri",
    blocos=[
      ("Manhã", "Começem pelo Parque do Retiro: lago do Estanque e o Palácio de Cristal. Saiam pela Puerta de Alcalá e desçam até Cibeles. O mirante do Palacio de Cibeles (CentroCentro) abre na sexta e tem a melhor vista da Gran Vía.", ["Retiro", "Puerta de Alcalá", "Cibeles"]),
      ("Almoço", "Barrio de las Letras: tapas no balcão da Cervecería Cervantes, a 5 minutos do Prado.", ["Cervecería Cervantes"]),
      ("Tarde", "Passeio pelo Barrio de las Letras (as ruas com citações no chão). Café no Acid Café. Às 17h30, fila do Prado: a entrada é <b>grátis de segunda a sábado das 18h às 20h</b>, o que economiza €75 para os 5.", ["Acid Café", "Prado"]),
      ("Noite", "La Casa del Abuelo (gambas al ajillo, balcão) perto de Sol.", ["Casa del Abuelo"]),
    ]),
  dict(data="2027-02-20", cidade="madri", titulo="Madri dos Áustrias, Palácio e pôr do sol", noite="Madri",
    blocos=[
      ("Manhã", "Puerta del Sol → Calle Mayor → Plaza Mayor → Plaza de la Villa → Catedral de la Almudena. Estejam no Palácio Real antes das 11h: <b>sábado tem a troca da guarda (11h–14h)</b>. Ingresso ~€18. Depois, os Jardines de Sabatini.", ["Puerta del Sol", "Almudena", "Palacio Real", "Sabatini"]),
      ("Almoço", "Cava Baja, em La Latina: Taberna La Concha para tapas. Se quiserem o clássico, o Botín (o restaurante mais antigo do mundo, cochinillo) pede reserva com semanas de antecedência.", ["Taberna La Concha", "Botín"]),
      ("Tarde", "Plaza de España e o Templo de Debod no pôr do sol (~18h50). Depois, Gran Vía: Primark, Zara e o terraço do El Corte Inglés de Callao (Gourmet Experience), com vista para a Gran Vía.", ["Templo de Debod", "Gran Vía (+", "Callao — terraço"]),
      ("Noite", "Mercado de San Miguel para petiscar em pé, a 2 minutos da Plaza Mayor.", ["Mercado de San Miguel"]),
    ]),
  dict(data="2027-02-21", cidade="roma", titulo="Voo para Roma e o centro a pé", noite="Roma",
    blocos=[
      ("Manhã", "Iberia 08:45 → Fiumicino 11:10 (ver Voos e trens). Saiam de casa ~6h30 de táxi ou Uber (tarifa fixa ~€33 por carro). De Fiumicino: trem regional FL1 + metrô sai ~€47,50 para os 5; o Leonardo Express, direto até Termini em 32 min, ~€70.", []),
      ("Atenção", "<b>Domingo muita coisa fecha</b>: Vaticano, mercado de Testaccio, CasaManco, Supplì Roma, Roscioli, Peroni e Formula 1. Por isso hoje é dia de rua e praça.", []),
      ("Tarde", "Panteão (€7), Piazza Navona com sorvete na Gelateria del Teatro, e a Fontana di Trevi. <b>A Trevi cobra €2 para chegar perto da fonte das 9h às 22h</b>; depois das 22h é grátis e mais vazia.", ["Panteão", "Piazza Navona", "Gelateria del Teatro", "Trevi"]),
      ("Noite", "Emma Pizzeria (reserve) ou Osteria da Fortunata no Panteão, onde fazem a massa na vitrine. Ambas abrem no domingo.", ["Emma", "Fortunata"]),
      ("Opcional", "Lazio × Napoli no Olímpico, domingo 15h (data provisória do campeonato).", ["Stadio Olimpico"]),
    ]),
  dict(data="2027-02-22", cidade="roma", titulo="Roma Antiga", noite="Roma",
    blocos=[
      ("Manhã", "Coliseu às 8h30, o primeiro horário (ingresso com hora marcada; <b>vendas abrem 30 dias antes</b>). Depois, Fórum Romano e Palatino com o mesmo ingresso. Contem 4 a 5 horas.", ["Coliseu"]),
      ("Almoço", "La Taverna dei Quaranta, ao lado do Coliseu. Reservem para 5.", ["Taverna dei Quaranta"]),
      ("Tarde", "Circo Massimo e subida ao Vittoriano: o elevador panorâmico do terraço tem a vista de Roma inteira. Depois, Monti para um sorvete no Fatamorgana.", ["Circo Massimo", "Vittoriano", "Fatamorgana"]),
      ("Noite", "Il Grottino a Testaccio, pizza romana fininha. Aceita reserva e hoje abre (fecha na terça).", ["Il Grottino"]),
      ("Por que hoje", "Segunda-feira a Galleria Borghese e o Castel Sant'Angelo fecham. A Roma Antiga abre todo dia.", []),
    ]),
  dict(data="2027-02-23", cidade="roma", titulo="Vaticano e Prati", noite="Roma",
    blocos=[
      ("Manhã", "Museus Vaticanos e Capela Sistina no primeiro horário (<b>reservem assim que abrir, ~2 meses antes</b>, só em tickets.museivaticani.va). Depois, Basílica de São Pedro e a cúpula (551 degraus, ou elevador + 320).", ["Museus Vaticanos", "Basílica de São Pedro"]),
      ("Almoço", "Pizzarium do Bonci, pizza al taglio, a 10 min a pé dos Museus. O Panificio Bonci fica ao lado.", ["Pizzarium", "Panificio Bonci"]),
      ("Tarde", "Se forem à audiência de amanhã, retirem os ingressos no Portão de Bronze (terça 15h–19h). Castel Sant'Angelo (aberto hoje) e sorvete na Gelateria dei Gracchi, em Prati.", ["Audiência", "Castel Sant'Angelo", "Gracchi"]),
      ("Noite", "San Lorenzo, o bairro universitário: Pizzeria Formula 1 ou L'Economica, as duas baratas e sem reserva.", ["Formula 1", "L'Economica"]),
    ]),
  dict(data="2027-02-24", cidade="roma", titulo="Papa, Testaccio e Trastevere", noite="Roma",
    blocos=[
      ("Manhã (opcional)", "Audiência geral do Papa às quartas de manhã, grátis com ingresso pedido ~1 mês antes. <b>A Basílica de São Pedro fica fechada até o fim da audiência.</b> Sem audiência: Aventino e o buraco da fechadura dos Cavaleiros de Malta.", ["Audiência"]),
      ("Almoço", "Mercato di Testaccio: pizza da CasaManco. O mercado funciona de manhã até o começo da tarde, então cheguem até 13h.", ["Mercato di Testaccio", "CasaManco"]),
      ("Tarde", "Trastevere a pé: Santa Maria in Trastevere, Supplì Roma, sorvete na Alla Scala ou na Fiordiluna.", ["Trastevere", "Supplì Roma", "Alla Scala", "Fiordiluna"]),
      ("Noite", "Antica Osteria Rugantino (reserve; quarta só no jantar) ou Da Vittorio a Trastevere, que é pequena e pede ligação antes. Trapizzino na Piazza Trilussa para a saideira.", ["Rugantino", "Da Vittorio", "Trapizzino"]),
    ]),
  dict(data="2027-02-25", cidade="roma", titulo="Borghese, Spagna e o centro das compras", noite="Roma",
    blocos=[
      ("Manhã", "Galleria Borghese no turno das 9h (<b>reserva obrigatória</b>, turnos de exatamente 2h, sem venda na porta). Depois, Villa Borghese e o Pincio, descendo para a Piazza del Popolo, com café no Sensorio Coffee Lab.", ["Galleria Borghese", "Sensorio"]),
      ("Almoço", "All'Antico Vinaio na Via del Corso (schiacciata recheada, fila anda rápido).", ["Via del Corso"]),
      ("Tarde", "Piazza di Spagna e tiramisù no Pompi. Depois, Campo de' Fiori (a feira vai até o começo da tarde) e o balcão do Antico Forno Roscioli.", ["Piazza di Spagna", "Pompi", "Campo de' Fiori", "Roscioli"]),
      ("Noite", "L'Antica Birreria Peroni, perto da Trevi: salsicha, cerveja e preço honesto. Reservem para 5.", ["Peroni"]),
    ]),
  dict(data="2027-02-26", cidade="verona", titulo="Trem para Verona", noite="Verona",
    blocos=[
      ("Manhã", "Italo 8956, Roma Termini 08:20 → Verona Porta Nuova 11:38, direto (ver Transporte: <b>já dá para comprar</b>). Da estação ao centro são ~20 min a pé ou ônibus 11/12/13/51/52.", []),
      ("Tarde", "Arena (€12), Via Mazzini, Casa di Giulietta (<b>só com horário reservado desde abril de 2026</b>: €5 o pátio, €12 com a casa), Piazza delle Erbe e a Torre dei Lamberti no fim da tarde.", ["Arena", "Giulietta", "Piazza delle Erbe e", "Lamberti"]),
      ("Noite", "Osteria al Duca (menu fixo ~€26–30) ou, barato, pizza no Du de Cope.", ["al Duca", "Du de Cope"]),
    ]),
  dict(data="2027-02-27", cidade="verona", titulo="Bate-volta a Veneza", noite="Verona",
    blocos=[
      ("Dia", "Trem regional até Venezia Santa Lucia (~1h25, €11–14 por pessoa por trecho) ou Frecciarossa/Italo (~1h10). A taxa de acesso a Veneza em 2024–2026 só valeu entre abril e julho, então 27/02 deve estar livre: confirmem o calendário de 2027 em janeiro.", ["Veneza"]),
      ("Alternativa", "Ficar em Verona: Castelvecchio e Ponte Scaligero, Basílica de San Zeno, e o funicular até o Castel San Pietro no pôr do sol. Sirmione no inverno tem muita coisa fechada.", ["Castelvecchio", "San Zeno", "Castel San Pietro"]),
      ("Noite", "De volta a Verona: Trattoria Al Pompiere (reserve) ou Osteria Sottoriva, debaixo dos arcos.", ["Al Pompiere", "Sottoriva"]),
    ]),
  dict(data="2027-02-28", cidade="innsbruck", titulo="Alpes pelo Brenner", noite="Innsbruck",
    blocos=[
      ("Manhã", "Railjet 88, Verona 09:01 → Innsbruck 12:32, direto pelo Passo do Brenner (ver Transporte: venda abre ~meados de outubro).", []),
      ("Tarde", "O museu do Telhado de Ouro <b>fecha às segundas no inverno</b>, então é hoje, antes das 17h. Depois, Hofburg (€15) e a Maria-Theresien-Strasse com a vista das montanhas. Domingo as lojas fecham.", ["Telhado de Ouro", "Hofburg Innsbruck", "Maria-Theresien"]),
      ("Noite", "Gasthaus Goldenes Dachl ou Stiftskeller, comida tirolesa. Reservem para 5.", ["Gasthaus Goldenes", "Stiftskeller"]),
    ]),
  dict(data="2027-03-01", cidade="viena", titulo="Nordkette e trem para Viena", noite="Viena",
    blocos=[
      ("Manhã", "Deixem as malas no guarda-volumes da estação e subam a Nordkette às 9h: do centro até ~2.000 m, com neve. Ida e volta €50,40 até Seegrube ou €56 até Hafelekar. Voltem até 11h45.", ["Nordkette"]),
      ("Tarde", "Railjet Innsbruck 13:58 → Viena 18:32, direto (ou 12:56 → 17:32 para chegar mais cedo).", []),
      ("Noite", "Figlmüller, o schnitzel maior que o prato. O Schnitzelwirt fecha na segunda.", ["Figlmüller"]),
    ]),
  dict(data="2027-03-02", cidade="viena", titulo="Kipferl, Schönbrunn e a Prefeitura no gelo", noite="Viena",
    blocos=[
      ("Café da manhã", "Kipferl (ou croissant) com Melange no Joseph Brot, que abre às 7h30. O croissant descende do Kipferl vienense: a história de 1683 é lenda, e a ligação documentada é a padaria vienense de August Zang em Paris, por volta de 1838. Saindo, a 2 minutos: o Monumento contra a Guerra e o Fascismo, de Hrdlicka, na Albertinaplatz, e a Ópera por fora.", ["Joseph Brot", "Mahnmal", "Wiener Staatsoper (Ópera"]),
      ("Manhã", "Metrô U4 de Karlsplatz até Schönbrunn. Palácio às 8h30 (Palace Ticket ~€42, horário marcado, comprem 1–3 dias antes), depois os jardins e a subida até a Gloriette.", ["Schönbrunn"]),
      ("Almoço", "U4 até Kettenbrückengasse: almoço no Naschmarkt, que abre na terça.", ["Naschmarkt"]),
      ("Tarde", "Café no Sperl, a 5 minutos (o Central está fechado em obra). Depois, Kunsthistorisches Museum (€22, aberto na terça) ou, mais leve, o pátio do MuseumsQuartier em frente.", ["Sperl", "Kunsthistorisches", "MuseumsQuartier"]),
      ("Fim de tarde", "A pé pelo Ring (10 min) até a Rathausplatz: a Prefeitura iluminada e a pista de gelo <b>Wiener Eistraum</b>, que vai até 07/03, todo dia das 10h às 22h. Patinar ~1h (~€10,50) ou só passear com um Punsch quente.", ["Eistraum", "Wiener Rathaus"]),
      ("Jantar", "Café Landtmann, a 3 minutos (reservem para 5), com <b>Kaiserschmarrn</b>, a \"sobremesa do imperador\". Plano B: Heindl's, especialista em Kaiserschmarrn, ou a roda-gigante do Prater.", ["Landtmann", "Heindl"]),
    ]),
  dict(data="2027-03-03", cidade="viena", titulo="Klimt e o centro imperial", noite="Viena",
    blocos=[
      ("Manhã", "Belvedere Superior às 9h, onde está O Beijo de Klimt (€23, horário marcado; comprem 1–3 dias antes).", ["Belvedere"]),
      ("11h", "A pé (~15 min) até a Karlskirche.", ["Karlskirche"]),
      ("Almoço", "Trzesniewski, os sanduichinhos abertos vienenses, em pé e baratos. A uma quadra, o Gragger vende Kipferl de forno a lenha para levar (abre de terça a sábado).", ["Trzesniewski", "Gragger"]),
      ("13h", "Stephansplatz e a Stephansdom (visita turística 13h–16h30; torre opcional, €8). Depois, o Graben com a Coluna da Peste. Para comparar croissant: Felber, na Tuchlauben, a 2 minutos.", ["Catedral de Santo Estêvão", "Graben", "Felber"]),
      ("15h", "Peterskirche: <b>concerto de órgão grátis às 15h</b> (30 min, por doação; entrem às 14h50). Depois, o Kohlmarkt até a Michaelerplatz e o Kaisertor da Hofburg.", ["Peterskirche", "Kohlmarkt"]),
      ("15h45", "Museu Sisi + Apartamentos Imperiais + Coleção de Prata (~€20, horário marcado no site oficial; entrada pelo Kaisertor; o percurso renovado reabre em 19/11/2026). Contem 1h30–2h.", ["Museu Sisi"]),
      ("Lanche", "Demel, aberto até 19h, com fila menor no fim da tarde: Annatorte ou Eduard-Sacher-Torte, e um Kaiserschmarrn para dividir.", ["Demel"]),
      ("Noite", "Jantar no Zwölf-Apostelkeller, uma adega medieval. Ou a roda-gigante do Prater iluminada. De sobremesa, Café Hawelka: as Buchteln saem do forno a partir das 20h. Durmam cedo: o trem sai às 07:40.", ["Zwölf-Apostelkeller", "Riesenrad", "Hawelka"]),
      ("Opcional", "A visita grátis por dentro da Prefeitura é só segunda, quarta e sexta às 13h, com inscrição online. Para fazer, troquem pela Stephansdom.", ["Wiener Rathaus"]),
    ]),
  dict(data="2027-03-04", cidade="budapeste", titulo="Trem para Budapeste e o bairro judeu", noite="Budapeste",
    blocos=[
      ("Manhã", "Railjet Viena 07:40 → Budapest-Keleti 10:35 (ver Transporte). Confiram que o trem vai até Keleti, e não só até Kelenföld.", []),
      ("Tarde", "Sinagoga da Rua Dohány: <b>fecha no sábado e fecha cedo na sexta</b>, então é hoje. Bairro judeu, Szimpla Kert, e a Basílica de Santo Estêvão com o mirante no fim da tarde.", ["Sinagoga", "Szimpla", "Basílica de Santo Estêvão"]),
      ("Noite", "Cruzeiro de 1h no Danúbio (Legenda), com o Parlamento iluminado. Jantar barato no Frici Papa.", ["Cruzeiro", "Frici Papa"]),
      ("Dinheiro", "A Hungria usa florim (HUF). Paguem no cartão em HUF, recusem a conversão para real ou euro na maquininha, e evitem os caixas Euronet.", []),
    ]),
  dict(data="2027-03-05", cidade="budapeste", titulo="Parlamento, Buda e os banhos", noite="Budapeste",
    blocos=[
      ("Manhã", "Visita ao Parlamento (~€35, <b>reservem 1–2 semanas antes</b>; audioguia em português). Depois, o memorial dos Sapatos na Margem do Danúbio e a Ponte das Correntes.", ["Parlamento", "Sapatos"]),
      ("Almoço", "Mercado Central: páprica e lembranças no térreo, lángos (pão frito húngaro) nas barracas do andar de cima. Alternativas: Retró Lángos ou comida caseira no Kisharang.", ["Mercado Central", "Retró Lángos", "Kisharang"]),
      ("Tarde", "Funicular até o Castelo de Buda, o Bastião dos Pescadores (as torres de cima só cobram a partir de meados de março) e a Igreja de Matias. No fim da tarde, os banhos Széchenyi (~€37 na sexta; comprem online para evitar fila). O Gellért está fechado para obras até 2028/29.", ["Castelo de Buda", "Bastião", "Igreja de Matias", "Széchenyi"]),
      ("Noite", "Jantar no Hungarikum Bisztró (goulash e paprikás).", ["Hungarikum"]),
    ]),
  dict(data="2027-03-06", cidade="madri", titulo="Voo de volta a Madri", noite="Madri",
    blocos=[
      ("Manhã", "Iberia 11:10 → Madri 14:30. Saiam ~8h30 com o ônibus 100E até o aeroporto (2.500 HUF por pessoa, o passe comum não vale nele).", []),
      ("Tarde", "Chegada às 14:30. Táxi ou Uber até a hospedagem (tarifa fixa ~€33). Recolham as malas grandes e descansem: amanhã é dia cheio.", []),
      ("Noite", "Jantar leve perto de casa: tapas em La Latina ou o Mercado de San Fernando, em Lavapiés.", ["San Fernando"]),
    ]),
  dict(data="2027-03-07", cidade="madri", titulo="Rastro, montaditos a €1 e Toledo", noite="Madri",
    blocos=[
      ("Manhã", "El Rastro, a feira de domingo (9h–15h): é gigante e se espalha por La Latina e Embajadores, quase conectando um lado da cidade ao outro. Vale ir sem pressa.", ["El Rastro"]),
      ("Almoço", "<b>Domingo é dia de Euromanía no 100 Montaditos</b>: quase tudo a €1. A unidade da Calle San Millán 6 fica colada ao Rastro.", ["100 Montaditos"]),
      ("Tarde", "Bate-volta curto a Toledo (trem Avant de Atocha, 33 min, €13–16 o trecho; comprem antes, lota no fim de semana) ou tarde livre: Retiro de novo, compras na Gran Vía. O tour do Bernabéu ficou de fora: caro demais para 5.", ["Toledo"]),
      ("Noite", "Mercado de San Leopoldo ou Casa Dani, a tortilla famosa.", ["Mercado de San Leopoldo", "Casa Dani"]),
    ]),
  dict(data="2027-03-08", cidade="madri", titulo="Último dia e voo para casa", noite=None,
    blocos=[
      ("Manhã", "Checkout com as malas guardadas. Museu Reina Sofía, onde está a Guernica (aberto na segunda). Compras no El Corte Inglés de Preciados.", ["Museo Reina Sofía", "Corte Inglés Preciados +"]),
      ("Tarde", "O Palácio Real é grátis para brasileiros de segunda a quinta das 16h às 18h (com passaporte, fila ~1h antes). Só vale se as malas já estiverem com vocês: <b>hoje é o Dia da Mulher, as marchas fecham o centro à noite</b>.", ["Palacio Real"]),
      ("Noite", "Saiam para o aeroporto por volta das 17h, de táxi ou Uber: com as marchas do Dia da Mulher o centro fica fechado e o trânsito pesa, então peçam o carro numa rua fora do trajeto das marchas. CA897 às 22:30 → Guarulhos 05:30.", []),
    ]),
]

# O que fica de fora do dia a dia, mas esta na lista do Lucas: aparece na pagina
# da cidade com o motivo.
FORA = {
  "roma": [
    ("Tiramisù di Forattini", "Fica em Torrenova, ~45 min de metrô C do centro. O Pompi (25/02) é a alternativa central."),
    ("Trattoria Guerra", "Nomentano, fora do caminho e com ~15 lugares. Vale se sobrar uma noite."),
    ("Grano, Frutta e Farina", "Campo Marzio: encaixa no dia 25/02, perto da Piazza di Spagna."),
    ("Il Pastaio", "Perto da Piazza Navona: encaixa no dia 21/02 ou 25/02."),
    ("I Caruso", "Perto da Via XX Settembre; talvez feche domingo. Encaixa no dia 23/02 a caminho de San Lorenzo."),
    ("San Crispino", "Pode ter fechado; confiram no Google Maps antes."),
    ("Maddalena", "A outra unidade do All'Antico Vinaio, ao lado do Panteão (21/02)."),
    ("Porta Maggiore", "Perto de San Lorenzo: dá para passar no dia 23/02 à noite."),
  ],
  "madri": [
    ("Kitchen 154", "Mercado de Vallehermoso (Chamberí). Fecha segunda e terça."),
    ("Hundred", "Hambúrguer em Chueca. Horário não confirmado."),
  ],
}


# DICAS DE QUEM JA FOI — palavras do Lucas, da viagem de fevereiro de 2026.
DICAS = {
  "madri": [
    "No aeroporto, dá para pedir táxi na saída para quantas pessoas precisar.",
    "Para pegar Uber: na rampa à direita, antes de sair para a rua, subam até o estacionamento.",
    "Chegando de noite, vai estar tudo fechado. Vejam algo perto ou peçam pelo Uber Eats.",
    "O metrô é barato, tranquilo e tem muitas linhas. Um cartão só serve para todo mundo.",
    "Tem muitos lockers (guarda-volumes) espalhados pela cidade.",
    "O Rastro, no domingo, é uma feira gigantesca que conecta quase a cidade inteira.",
    "A cidade é rápida de atravessar a pé: olhando em volta, quando você vê, já atravessou.",
    "O vento é frio nessa época.",
    "O tour do Santiago Bernabéu não compensa: caro demais para levar todo mundo.",
  ],
}
