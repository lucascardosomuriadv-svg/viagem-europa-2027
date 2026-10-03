# -*- coding: utf-8 -*-
"""Mais atrações por cidade (óbvias que faltavam + pouco conhecidas), com coordenada e foto livre.

    python fonte/atracoes.py

Cada candidato aponta para um artigo da Wikipédia ("en:Título", "de:…", "it:…", "hu:…", "es:…").
De lá vêm a coordenada e a foto principal; autor e licença vêm do Wikimedia Commons.
Quem fica sem foto livre NÃO entra (a regra é: toda atração com foto). Grava
`pesquisa/atracoes-extra.json` e `pesquisa/fotos-avulsas.json` (fotos para lugares que já existiam).
"""
import json, pathlib, re, sys, time, urllib.error, urllib.parse, urllib.request
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
AQUI = pathlib.Path(__file__).parent
PESQ = AQUI / "pesquisa"
UA = {"User-Agent": "guia-viagem-europa-2027/1.0 (uso pessoal; github.com/lucascardosomuriadv-svg)"}

# (nome no guia, artigo, o que é, uma linha de dica)
C = {
"madri": [
 ("Palacio de Cristal (Retiro)", "en:Palacio de Cristal del Retiro", "pavilhão de vidro dentro do Retiro", "Entrada grátis; fica à beira de um laguinho"),
 ("Estação de Atocha (jardim tropical)", "en:Madrid Atocha railway station", "estação com jardim de palmeiras", "O jardim fica no saguão antigo; de lá sai o trem para Toledo"),
 ("Real Jardín Botánico", "en:Real Jardín Botánico de Madrid", "jardim botânico ao lado do Prado", "Estufas quentes, bom para um dia frio"),
 ("CaixaForum (jardim vertical)", "en:CaixaForum Madrid", "centro cultural com parede de plantas", "O jardim vertical fica na rua, não paga"),
 ("Círculo de Bellas Artes (terraço)", "en:Círculo de Bellas Artes", "terraço com vista da Gran Vía", "Uma das melhores vistas do Edifício Metrópolis"),
 ("Plaza de Oriente", "en:Plaza de Oriente", "praça em frente ao Palácio Real", "Estátuas dos reis e o Teatro Real"),
 ("Plaza de la Villa", "en:Plaza de la Villa", "praça medieval", "Pequena e quieta, a dois passos da Plaza Mayor"),
 ("Plaza de Santa Ana (Barrio de las Letras)", "en:Plaza de Santa Ana", "praça de bares", "O bairro dos escritores; frases de livros no chão das ruas"),
 ("Monasterio de las Descalzas Reales", "en:Convent of Las Descalzas Reales", "convento real com obras de arte", "Só com visita guiada; pouca gente conhece"),
 ("San Francisco el Grande", "en:Basilica of San Francisco el Grande, Madrid", "basílica com cúpula enorme", "Uma das maiores cúpulas da Europa"),
 ("Ermita de San Antonio de la Florida", "en:Royal Chapel of St. Anthony of La Florida", "capela com afrescos de Goya", "Grátis; Goya está enterrado ali"),
 ("Museo Sorolla", "en:Sorolla Museum", "casa-museu do pintor Sorolla", "Casa com jardim; confiram se já reabriu da reforma"),
 ("Museo Cerralbo", "en:Cerralbo Museum", "palacete do século XIX", "Casa de marquês intacta, perto da Plaza de España"),
 ("Palacio de Liria", "en:Liria Palace", "palácio da Casa de Alba", "Visita com hora marcada; Goya e Velázquez na parede"),
 ("Museo Arqueológico Nacional", "en:National Archaeological Museum (Madrid)", "museu de arqueologia", "A Dama de Elche está aqui"),
 ("Campo del Moro", "en:Campo del Moro", "jardim atrás do Palácio Real", "A melhor foto do palácio, de baixo; grátis"),
 ("Madrid Río", "en:Madrid Río", "parque na beira do rio Manzanares", "Passeio plano com pontes modernas"),
 ("Matadero Madrid", "en:Matadero Madrid", "antigo matadouro, hoje centro cultural", "Exposições grátis; fica no Madrid Río"),
 ("Teleférico de Madrid", "en:Teleférico de Madrid", "teleférico até a Casa de Campo", "Vista do Palácio Real de cima; confiram se funciona em fevereiro"),
 ("Faro de Moncloa", "en:Faro de Moncloa", "torre-mirante de 92 m", "Mirante envidraçado, barato"),
 ("Estação fantasma de Chamberí", "es:Estación de Chamberí", "estação de metrô de 1919 parada no tempo", "Grátis; abre mais no fim de semana"),
 ("Las Ventas", "en:Las Ventas", "praça de touros em estilo mourisco", "Vale pela fachada; metrô Ventas"),
 ("Parque de El Capricho", "en:Parque de El Capricho", "jardim romântico pouco conhecido", "Só abre sábado e domingo"),
 ("Bate-volta Segóvia", "en:Aqueduct of Segovia", "aqueduto romano e castelo", "Trem rápido de Chamartín, ~30 min"),
 ("Bate-volta El Escorial", "en:El Escorial", "mosteiro-palácio de Felipe II", "Trem ou ônibus, ~1h; fecha às segundas"),
],
"roma": [
 ("Piazza del Popolo", "en:Piazza del Popolo", "praça com obelisco e igrejas gêmeas", "Santa Maria del Popolo tem dois Caravaggios, grátis"),
 ("Terrazza del Pincio", "en:Pincian Hill", "mirante sobre a Piazza del Popolo", "Pôr do sol com a cúpula de São Pedro ao fundo"),
 ("Jardim das Laranjeiras (Giardino degli Aranci)", "it:Giardino degli Aranci", "jardim com mirante no Aventino", "Vista do Tibre e de São Pedro; grátis"),
 ("Buraco da fechadura do Aventino", "en:Villa del Priorato di Malta", "a cúpula de São Pedro pela fechadura", "Fica ao lado do Jardim das Laranjeiras; tem fila curta"),
 ("Bocca della Verità", "en:Bocca della Verità", "a máscara de mármore do filme", "Fica na entrada de Santa Maria in Cosmedin"),
 ("São João de Latrão", "en:Archbasilica of Saint John Lateran", "a catedral de Roma", "Grátis; a Scala Santa fica em frente"),
 ("Santa Maria Maggiore", "en:Santa Maria Maggiore", "basílica com mosaicos do século V", "Grátis; perto da estação Termini"),
 ("San Pietro in Vincoli", "en:San Pietro in Vincoli", "igreja do Moisés de Michelangelo", "Grátis; a 5 min do Coliseu"),
 ("Santa Maria in Trastevere", "en:Santa Maria in Trastevere", "basílica de mosaicos dourados", "A praça em frente é o coração do Trastevere"),
 ("San Luigi dei Francesi", "en:San Luigi dei Francesi", "igreja com três Caravaggios", "Grátis; entre o Panteão e a Piazza Navona"),
 ("Sant'Ignazio", "en:Sant'Ignazio, Rome", "igreja com teto em ilusão de ótica", "A cúpula é pintada; tem um espelho para ver o teto"),
 ("Santa Maria della Vittoria", "en:Santa Maria della Vittoria, Rome", "igreja do Êxtase de Santa Teresa", "A escultura de Bernini; grátis"),
 ("Basílica de San Clemente", "en:Basilica of San Clemente al Laterano", "igreja em três níveis", "Desce-se até uma casa romana; perto do Coliseu"),
 ("Piazza del Campidoglio", "en:Piazza del Campidoglio", "praça desenhada por Michelangelo", "Atrás dela, vista do Fórum Romano de graça"),
 ("Museus Capitolinos", "en:Capitoline Museums", "museu no Campidoglio", "A Loba Capitolina e a vista do Fórum"),
 ("Mercados de Trajano", "en:Trajan's Market", "o shopping da Roma antiga", "Dá para ver boa parte da rua, sem pagar"),
 ("Termas de Caracalla", "en:Baths of Caracalla", "ruínas de termas gigantes", "Pouca fila; perto do Circo Massimo"),
 ("Via Appia Antica", "en:Appian Way", "a estrada romana e as catacumbas", "Melhor no domingo, quando fecha para carros"),
 ("Gianicolo (mirante)", "en:Janiculum", "morro com vista de Roma inteira", "Ao meio-dia dispara um canhão"),
 ("Fontana dell'Acqua Paola", "en:Fontana dell'Acqua Paola", "o fontanone do Gianicolo", "Fonte monumental com mirante"),
 ("Quartiere Coppedè", "it:Quartiere Coppedè", "quarteirão de arquitetura fantástica", "Pouco turista; parece cenário de filme"),
 ("Pirâmide de Céstio", "en:Pyramid of Cestius", "pirâmide romana de 12 a.C.", "Ao lado do Testaccio e do cemitério dos poetas"),
 ("Largo di Torre Argentina", "en:Largo di Torre Argentina", "ruínas onde César foi morto", "Hoje é um santuário de gatos"),
 ("Gueto Judeu e Pórtico de Otávia", "en:Porticus Octaviae", "bairro judeu de Roma", "A alcachofra frita (carciofo alla giudia) é daqui"),
 ("Ilha Tiberina", "en:Tiber Island", "ilha no meio do Tibre", "Caminho bonito entre o Gueto e o Trastevere"),
 ("Fontana delle Tartarughe", "en:Fontana delle Tartarughe", "fonte das tartarugas", "Escondida numa pracinha do Gueto"),
 ("Galleria Doria Pamphilj", "en:Doria Pamphilj Gallery", "palácio com galeria de espelhos", "Velázquez e Caravaggio, sem multidão"),
 ("Galleria Sciarra", "it:Galleria Sciarra", "pátio coberto com afrescos Art Nouveau", "Grátis, a 2 min da Fontana di Trevi"),
 ("Cripta dos Capuchinhos", "en:Capuchin Crypt", "capelas decoradas com ossos", "Na Via Veneto; impressiona"),
 ("Centrale Montemartini", "en:Centrale Montemartini", "estátuas romanas numa usina elétrica", "Museu vazio e diferente de tudo"),
 ("Colosseo Quadrato (EUR)", "en:Palazzo della Civiltà Italiana", "o Coliseu quadrado", "Bairro EUR, de metrô"),
 ("Bate-volta Ostia Antica", "en:Ostia Antica", "cidade romana em ruínas", "Trem de Piramide, ~30 min; fecha às segundas"),
 ("Bate-volta Tivoli (Villa d'Este)", "en:Villa d'Este", "jardins com centenas de fontes", "Trem ou ônibus, ~1h"),
],
"verona": [
 ("Ponte Pietra", "en:Ponte Pietra (Verona)", "ponte romana sobre o Ádige", "A vista mais bonita é no fim da tarde"),
 ("Teatro Romano", "en:Roman theatre, Verona", "teatro romano na encosta", "Museu arqueológico em cima, com vista"),
 ("Duomo de Verona", "en:Verona Cathedral", "catedral românica", "Tem um Ticiano no altar lateral"),
 ("Sant'Anastasia", "en:Sant'Anastasia (Verona)", "a maior igreja gótica da cidade", "O afresco de Pisanello fica no alto"),
 ("San Fermo Maggiore", "en:San Fermo Maggiore, Verona", "duas igrejas, uma sobre a outra", "O teto de madeira parece um casco de navio"),
 ("Giardino Giusti", "en:Giardino Giusti", "jardim renascentista", "Labirinto e mirante no alto"),
 ("Arche Scaligere", "en:Scaliger Tombs", "túmulos góticos dos senhores de Verona", "Dá para ver da rua, de graça"),
 ("Porta Borsari", "en:Porta Borsari", "portão romano do século I", "No meio da rua de comércio"),
 ("Arco dei Gavi", "en:Arco dei Gavi", "arco romano ao lado do Castelvecchio", ""),
 ("Ponte Scaligero", "en:Castelvecchio Bridge", "ponte fortificada medieval", "Atravessar a pé; boa para fotos"),
 ("Piazza Bra", "en:Piazza Bra", "a praça da Arena", "O Liston é o calçadão dos cafés"),
 ("Via Mazzini", "it:Via Mazzini (Verona)", "rua de compras", "Liga a Piazza Bra à Piazza delle Erbe"),
 ("Tomba di Giulietta", "it:Tomba di Giulietta", "o túmulo da lenda", "Num convento com museu de afrescos"),
 ("Casa di Romeo", "it:Casa di Romeo", "casa medieval dos Montecchi", "Só por fora"),
 ("Santuário de Lourdes (mirante)", "it:Santuario della Madonna di Lourdes di Verona", "mirante mais alto da cidade", "De táxi ou ônibus; pôr do sol"),
 ("Bate-volta Borghetto sul Mincio", "it:Borghetto (Valeggio sul Mincio)", "vilarejo de moinhos", "Tortellini de Valeggio; melhor de carro ou táxi"),
 ("Bate-volta Mântua", "en:Mantua", "cidade dos Gonzaga", "Trem direto, ~45 min"),
 ("Bate-volta Pádua (Capela Scrovegni)", "en:Scrovegni Chapel", "os afrescos de Giotto", "Trem ~45 min; a capela exige reserva"),
 ("Bate-volta Vicenza", "en:Teatro Olimpico", "a cidade de Palladio", "Trem ~30 min"),
 ("Bate-volta Soave", "en:Soave, Veneto", "vila murada do vinho branco", "Trem até San Bonifacio, ~20 min"),
],
"innsbruck": [
 ("Schloss Ambras", "en:Ambras Castle", "castelo renascentista", "O Salão Espanhol e o gabinete de curiosidades"),
 ("Helblinghaus", "en:Helbling House", "fachada rococó", "Em frente ao Telhado de Ouro"),
 ("Museu de Arte Popular Tirolesa", "en:Tyrolean Folk Art Museum", "museu de cultura tirolesa", "O ingresso vale também para a Hofkirche"),
 ("Ferdinandeum", "en:Tyrolean State Museum", "museu estadual do Tirol", ""),
 ("Basílica de Wilten", "de:Basilika Wilten", "igreja rococó", "Interior dourado; ao pé do Bergisel"),
 ("Abadia de Wilten", "de:Stift Wilten", "abadia barroca", "Ao lado da basílica"),
 ("Tirol Panorama", "de:Das Tirol Panorama", "pintura gigante em 360°", "No Bergisel; a batalha de 1809"),
 ("Hofgarten", "de:Hofgarten (Innsbruck)", "parque ao lado da Hofburg", "Grátis"),
 ("Hungerburg (mirante)", "en:Hungerburgbahn", "funicular de Zaha Hadid", "Só até a Hungerburg sai bem mais barato que subir a Nordkette"),
 ("Fundição de sinos Grassmayr", "en:Grassmayr Bell Foundry", "museu dos sinos, família desde 1599", "Dá para tocar os sinos; pouco conhecido"),
 ("Igreja dos Jesuítas", "de:Jesuitenkirche (Innsbruck)", "igreja barroca da universidade", ""),
 ("Ottoburg", "de:Ottoburg", "torre residencial de 1494", "Na ponta da Cidade Velha, à beira do rio"),
 ("Patscherkofel", "en:Patscherkofel", "montanha do outro lado do vale", "Teleférico moderno; vista da cidade e da Nordkette"),
 ("Bate-volta Hall in Tirol", "en:Hall in Tirol", "cidade medieval a 10 min de trem", "Centro histórico maior que o de Innsbruck e sem turista"),
 ("Bate-volta Seefeld", "en:Seefeld in Tirol", "vila alpina num platô", "Trem ~35 min; paisagem de neve"),
],
"viena": [
 ("Hundertwasserhaus", "en:Hundertwasserhaus", "prédio colorido e torto", "Só por fora; a Kunst Haus Wien fica perto"),
 ("Biblioteca Nacional (Prunksaal)", "en:Austrian National Library", "salão barroco de livros", "Uma das bibliotecas mais bonitas do mundo"),
 ("Votivkirche", "en:Votivkirche, Vienna", "igreja neogótica", "Grátis"),
 ("Parlamento", "en:Austrian Parliament Building", "prédio em estilo grego", "Visita grátis com reserva"),
 ("Burgtheater", "en:Burgtheater", "teatro nacional", "Em frente à prefeitura"),
 ("Volksgarten", "en:Volksgarten, Vienna", "jardim com templo de Teseu", ""),
 ("Stadtpark (Strauss dourado)", "en:Stadtpark, Vienna", "parque da estátua de Strauss", "A estátua mais fotografada de Viena"),
 ("Secession", "en:Secession Building", "pavilhão Art Nouveau", "O Friso de Beethoven, de Klimt, fica no subsolo"),
 ("Museu Leopold", "en:Leopold Museum", "Schiele e Klimt", "No MuseumsQuartier"),
 ("Museu de História Natural", "en:Natural History Museum, Vienna", "o gêmeo do Kunsthistorisches", "A Vênus de Willendorf está aqui"),
 ("Tesouro Imperial (Schatzkammer)", "en:Imperial Treasury, Vienna", "coroas e joias dos Habsburgo", "Dentro da Hofburg"),
 ("Cripta Imperial (Kaisergruft)", "en:Imperial Crypt", "túmulos dos Habsburgo", "Sisi e Francisco José estão aqui"),
 ("Escola Espanhola de Equitação", "en:Spanish Riding School", "os cavalos lipizzaners", "O treino da manhã é mais barato que a apresentação"),
 ("Mozarthaus", "en:Mozarthaus Vienna", "o apartamento de Mozart", "Atrás da catedral"),
 ("Haus der Musik", "en:Haus der Musik", "museu interativo de música", "Dá para reger a Filarmônica"),
 ("Ankeruhr", "de:Ankeruhr", "relógio Art Nouveau", "Ao meio-dia desfilam todas as figuras"),
 ("Palais Ferstel (passagem)", "en:Palais Ferstel", "galeria coberta", "O Café Central fica aqui"),
 ("Igreja dos Jesuítas", "en:Jesuit Church, Vienna", "igreja com cúpula pintada em ilusão", "Pouco visitada"),
 ("Palácio da Justiça (café no terraço)", "en:Palace of Justice, Vienna", "escadaria monumental", "Café no último andar, com vista e preço normal"),
 ("Pavilhões de Otto Wagner (Karlsplatz)", "en:Karlsplatz Stadtbahn Station", "estação Art Nouveau", "Em frente à Karlskirche"),
 ("Gloriette", "en:Gloriette", "mirante no alto de Schönbrunn", "A subida pelo jardim é grátis"),
 ("Zoológico de Schönbrunn", "en:Tiergarten Schönbrunn", "o zoológico mais antigo do mundo", "Tem pandas"),
 ("Haus des Meeres", "en:Haus des Meeres", "aquário numa torre antiaérea", "Terraço com vista"),
 ("Augarten", "en:Augarten", "parque barroco com torres antiaéreas", "Fábrica de porcelana ao lado"),
 ("Donauturm", "en:Donauturm", "torre-mirante de 252 m", ""),
 ("Kahlenberg (mirante)", "en:Kahlenberg", "morro com vista de Viena inteira", "Ônibus 38A"),
 ("Grinzing", "en:Grinzing", "vila das tabernas de vinho", "Bonde 38 até o fim"),
 ("Cemitério Central", "en:Vienna Central Cemetery", "túmulos de Beethoven, Schubert e Strauss", "Bonde 71"),
 ("Gasometer", "en:Gasometer, Vienna", "gasômetros que viraram prédios", "Metrô U3"),
 ("Museu Sigmund Freud", "en:Sigmund Freud Museum (Vienna)", "a casa e o consultório de Freud", ""),
 ("Bate-volta Bratislava", "en:Bratislava Castle", "a capital da Eslováquia", "Trem ~1h"),
 ("Bate-volta Abadia de Melk", "en:Melk Abbey", "abadia barroca sobre o Danúbio", "Trem ~1h"),
],
"budapeste": [
 ("Ponte das Correntes", "en:Széchenyi Chain Bridge", "a ponte mais famosa", "Bonita à noite, iluminada"),
 ("Ponte da Liberdade", "en:Liberty Bridge (Budapest)", "ponte verde de ferro", "Liga o Mercado Central ao Monte Gellért"),
 ("Monte Gellért e Cidadela", "en:Gellért Hill", "mirante com a Estátua da Liberdade", "A melhor vista do Danúbio; subida a pé"),
 ("Igreja na Rocha", "en:Gellért Hill Cave", "capela dentro de uma caverna", "Ao pé do Monte Gellért"),
 ("Avenida Andrássy", "en:Andrássy út", "o bulevar de Budapeste", "Do centro até a Praça dos Heróis"),
 ("Ópera de Budapeste", "en:Hungarian State Opera House", "ópera neorrenascentista", "Tem visita guiada"),
 ("Casa do Terror", "en:House of Terror", "museu das ditaduras nazista e comunista", "Fecha às segundas"),
 ("Ilha Margarida", "en:Margaret Island", "parque no meio do Danúbio", "Sem carros"),
 ("Rua Váci", "en:Váci Street", "calçadão de compras", "Turística; os preços são melhores fora dela"),
 ("Praça da Liberdade", "en:Liberty Square (Budapest)", "praça de prédios monumentais", "Entre o Parlamento e a Basílica"),
 ("Hospital na Rocha", "en:Hospital in the Rock", "hospital e bunker sob o castelo", "Só com visita guiada"),
 ("Biblioteca Szabó Ervin", "en:Metropolitan Ervin Szabó Library", "salas de palácio dentro de uma biblioteca", "Pouco conhecida; ingresso barato"),
 ("New York Café", "en:New York Café", "o café mais ornamentado da cidade", "Caro e com fila; vale espiar o salão"),
 ("Gozsdu Udvar", "hu:Gozsdu-udvar", "passagem de bares e restaurantes", "No bairro judeu"),
 ("Sinagoga da Rua Kazinczy", "hu:Kazinczy utcai zsinagóga", "sinagoga Art Nouveau", "A duas quadras do Szimpla"),
 ("Museu de Belas Artes", "en:Museum of Fine Arts (Budapest)", "museu na Praça dos Heróis", ""),
 ("Museu Nacional Húngaro", "en:Hungarian National Museum", "a história da Hungria", ""),
 ("Museu de Etnografia", "en:Museum of Ethnography (Budapest)", "prédio novo com telhado-jardim", "Dá para subir no telhado de graça"),
 ("Casa da Música Húngara", "en:House of Music Hungary", "prédio de vidro no parque", "Projeto de Sou Fujimoto"),
 ("Várkert Bazár", "hu:Várkert Bazár", "jardins e escadarias ao pé do castelo", "Escada rolante grátis até o castelo"),
 ("Estação Nyugati", "en:Budapest Nyugati station", "estação de ferro e vidro", "Construída pela empresa de Eiffel"),
 ("Metrô M1 (linha histórica)", "en:Line 1 (Budapest Metro)", "o metrô mais antigo do continente", "Estações de azulejo, sob a Andrássy"),
 ("Banhos Lukács", "en:Lukács Baths", "termas dos moradores", "Mais barato e vazio que o Széchenyi"),
 ("Mirante Erzsébet", "en:Elizabeth Lookout", "torre no ponto mais alto da cidade", "Sobe-se de teleférico de cadeirinha"),
 ("Memento Park", "en:Memento Park", "estátuas da era comunista", "Fora do centro, de ônibus"),
 ("Bate-volta Szentendre", "en:Szentendre", "vila de artistas no Danúbio", "Trem HÉV, ~40 min"),
],
}
# fotos para lugares que já estavam no guia e seguiam sem foto: prefixo do id -> artigo
AVULSAS = {
 "madri-museo-reina-sofia": "en:Museo Nacional Centro de Arte Reina Sofía", "madri-el-corte-ingles-callao": "en:Plaza del Callao",
 "madri-alcala-de-henares": "en:Alcalá de Henares", "verona-casa-di-giulietta": "en:Casa di Giulietta",
 "innsbruck-stadtturm": "de:Stadtturm (Innsbruck)", "viena-mahnmal": "de:Mahnmal gegen Krieg und Faschismus",
}
RUIM = re.compile(r"\.svg$|\.png$|\.gif$|\.tif|map|karte|logo|coat|wappen|stemma|escudo|flag|locator|plan\b|plano|diagram|grundriss|pianta|panoramio", re.I)
# coordenada à mão quando o artigo não devolve (conferidas no mapa)
COORD = {"Plaza de la Villa": (40.4153, -3.7103), "Museo Arqueológico Nacional": (40.4236, -3.6893), "Quartiere Coppedè": (41.9189, 12.5014),
 "Galleria Sciarra": (41.8998, 12.4816), "Bate-volta Tivoli (Villa d'Este)": (41.9631, 12.7961), "Piazza Bra": (45.4386, 10.9925),
 "Tomba di Giulietta": (45.4336, 10.9987), "Santuário de Lourdes (mirante)": (45.4530, 10.9950), "Bate-volta Soave": (45.4213, 11.2466),
 "Schloss Ambras": (47.2567, 11.4336), "Basílica de Wilten": (47.2536, 11.3997), "Abadia de Wilten": (47.2531, 11.4012),
 "Tirol Panorama": (47.2497, 11.3995), "Fundição de sinos Grassmayr": (47.2573, 11.3986), "Ottoburg": (47.2686, 11.3918),
 "Escola Espanhola de Equitação": (48.2075, 16.3661), "Ankeruhr": (48.2108, 16.3743), "Gloriette": (48.1783, 16.3087),
 "Zoológico de Schönbrunn": (48.1822, 16.3027), "Grinzing": (48.2567, 16.3414), "Sinagoga da Rua Kazinczy": (47.4983, 19.0619),
 "Casa da Música Húngara": (47.5133, 19.0822), "Várkert Bazár": (47.4947, 19.0411), "Metrô M1 (linha histórica)": (47.4969, 19.0508)}
CIDADE_EN = {"madri": "Madrid", "roma": "Rome", "verona": "Verona", "innsbruck": "Innsbruck", "viena": "Vienna", "budapeste": "Budapest"}
# lugar ao ar livre: a 2ª foto é outro ângulo, não "por dentro"
FORA = re.compile(r"praça|ponte|mirante|parque|jardim|rua|bate-volta|morro|ilha|avenida|bulevar|fonte|fontanone|arco|portão|túmulos|bairro|vila|montanha|teleférico|calçadão|quarteirão|estrada|pirâmide|ruínas|feira|torre-mirante|cidade|estátuas|fachada|pavilhões|relógio|funicular|máscara|cúpula de são pedro|pista|gasômetros", re.I)
# lugares antigos que são ao ar livre (2ª foto = outro ângulo)
ANTIGOS_FORA = {"madri-jardines-de-sabatini", "madri-templo-de-debod", "madri-parque-del-retiro", "madri-puerta-de-alcala", "madri-fuente-de-cibeles",
 "madri-gran-via", "madri-puerta-del-sol", "madri-el-rastro", "madri-bate-volta-a-toledo", "madri-el-corte-ingles-callao", "madri-alcala-de-henares",
 "roma-audiencia-geral", "roma-fontana-di-trevi", "roma-piazza-di-spagna", "roma-piazza-navona", "roma-circo-massimo", "roma-porta-maggiore",
 "roma-stadio-olimpico", "roma-trastevere", "roma-campo-de-fiori", "verona-castel-san-pietro", "verona-piazza-delle-erbe", "verona-bate-volta-veneza",
 "verona-bate-volta-sirmione", "innsbruck-nordkette", "innsbruck-goldenes-dachl", "innsbruck-bergisel", "innsbruck-maria-theresien", "innsbruck-altstadt",
 "innsbruck-stadtturm", "viena-naschmarkt", "viena-prater", "viena-museumsquartier", "viena-mahnmal", "viena-kohlmarkt", "viena-graben",
 "viena-wiener-eistraum", "budapeste-bastiao-dos-pescadores", "budapeste-cruzeiro-noturno", "budapeste-sapatos-na-margem", "budapeste-praca-dos-herois"}


def api(base, **p):
    p.update(format="json", formatversion="2")
    url = base + "?" + urllib.parse.urlencode(p)
    for t in range(6):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code != 429: raise
            time.sleep(int(e.headers.get("Retry-After") or 0) or 5 * (t + 1))
    raise SystemExit("Wikimedia continua limitando; rode de novo depois")


def limpa(h): return re.sub(r"<[^>]+>", "", h or "").strip()


def meta_de(ii):
    md = ii.get("extmetadata", {})
    return {"url": ii.get("thumburl") or ii["url"], "pagina": ii.get("descriptionurl"),
            "autor": limpa(md.get("Artist", {}).get("value"))[:80] or "Wikimedia Commons",
            "licenca": limpa(md.get("LicenseShortName", {}).get("value")) or "ver página"}


def artigos(refs):
    """{'en:Título': {'lat','lng','img'}} em lotes por idioma."""
    out, por_lang = {}, {}
    for r in refs: por_lang.setdefault(r.split(":", 1)[0], []).append(r.split(":", 1)[1])
    for lang, tits in por_lang.items():
        tits = sorted(set(tits))
        for i in range(0, len(tits), 20):
            lote = tits[i:i+20]
            q = api(f"https://{lang}.wikipedia.org/w/api.php", action="query", prop="coordinates|pageimages", piprop="name",
                    colimit="max", pilimit="max", titles="|".join(lote), redirects=1)["query"]
            alias = {n["from"]: n["to"] for n in q.get("normalized", [])}
            alias.update({n["from"]: n["to"] for n in q.get("redirects", [])})
            por = {pg["title"]: pg for pg in q["pages"]}
            for t in lote:
                alvo = alias.get(t, t); alvo = alias.get(alvo, alvo)
                pg = por.get(alvo) or {}
                co = (pg.get("coordinates") or [{}])[0]
                out[f"{lang}:{t}"] = {"lat": co.get("lat"), "lng": co.get("lon"), "img": pg.get("pageimage"), "falta": "missing" in pg}
            time.sleep(1)
    return out


def commons(arqs):
    meta = {}
    arqs = sorted(set(a for a in arqs if a))
    for i in range(0, len(arqs), 20):
        q = api("https://commons.wikimedia.org/w/api.php", action="query", prop="imageinfo", iiprop="url|extmetadata",
                iiurlwidth="800", titles="|".join("File:" + a for a in arqs[i:i+20]))["query"]
        for pg in q["pages"]:
            if "imageinfo" in pg: meta[pg["title"].removeprefix("File:").replace(" ", "_")] = meta_de(pg["imageinfo"][0])
        time.sleep(1)
    return meta


def busca(termo, fora=()):
    """Primeira foto boa do Commons para o termo (por relevância), que não seja uma das de `fora`."""
    q = api("https://commons.wikimedia.org/w/api.php", action="query", generator="search", gsrnamespace="6", gsrsearch=termo + " filetype:bitmap",
            gsrlimit="8", prop="imageinfo", iiprop="url|extmetadata|size|mime", iiurlwidth="800").get("query", {})
    for pg in sorted(q.get("pages", []), key=lambda p: p.get("index", 99)):
        ii = (pg.get("imageinfo") or [{}])[0]
        if ii.get("mime") != "image/jpeg" or ii.get("width", 0) < 900 or RUIM.search(pg["title"]): continue
        m = meta_de(ii)
        if m["url"] in fora: continue
        return m
    return None


def termo_de(ref, cid):
    t = re.sub(r"\s*\(.*?\)", "", ref.split(":", 1)[1]).replace(",", " ")
    c = CIDADE_EN[cid]
    return t if re.search(c + "|Madrid|Roma|Rome|Verona|Wien|Vienna|Budapest|Innsbruck", t, re.I) else f"{t} {c}"


def segunda(ref, cid, ao_ar_livre, f1):
    """(foto, 'por dentro' | '') — interior quando o lugar tem interior; senão outro ângulo."""
    t = termo_de(ref, cid)
    if not ao_ar_livre:
        f = busca(f"{t} interior", fora=(f1["url"],)); time.sleep(0.7)
        if f: return f, "por dentro"
    f = busca(t, fora=(f1["url"],)); time.sleep(0.7)
    return f, ""


def main():
    from fotos import ARTIGO
    antigos = {k: ("en:" + v) for k, v in ARTIGO.items()}       # lugares que já estavam no guia: prefixo do id -> artigo
    antigos.update(AVULSAS)
    refs = [a for l in C.values() for _, a, _, _ in l] + list(antigos.values())
    art = artigos(refs)
    meta = commons([v["img"] for v in art.values()])
    def foto(ref, cid):
        a = art[ref]
        if a["img"] and not RUIM.search(a["img"]) and a["img"].replace(" ", "_") in meta: return meta[a["img"].replace(" ", "_")]
        f = busca(termo_de(ref, cid)); time.sleep(0.7)      # foto principal ruim (logo, mapa) ou ausente
        return f
    saida, fora = {}, []
    for cid, lista in C.items():
        saida[cid] = []
        for nome, ref, tipo, dica in lista:
            a = art[ref]; f = foto(ref, cid)
            lat, lng = (a["lat"], a["lng"]) if a["lat"] is not None else COORD.get(nome, (None, None))
            if not f or lat is None:
                fora.append(f"{cid}: {nome} ({'sem foto' if not f else 'sem coordenada'})"); continue
            f2, rot = segunda(ref, cid, bool(FORA.search(tipo)), f)
            saida[cid].append({"nome": nome, "tipo": tipo, "dica": dica, "lat": round(lat, 5), "lng": round(lng, 5),
                               "fotos": [dict(f, rot="por fora" if rot else "")] + ([dict(f2, rot=rot)] if f2 else []), "wiki": ref})
        print(cid, len(saida[cid]), "atrações novas", flush=True)
    # lugares antigos: 1ª foto para os que não tinham, 2ª foto para todos
    velhas = {}
    for k, ref in antigos.items():
        cid = k.split("-")[0]
        f = foto(ref, cid)
        if not f: continue
        f2, rot = segunda(ref, cid, k in ANTIGOS_FORA, f)
        velhas[k] = [dict(f, rot="por fora" if rot else "")] + ([dict(f2, rot=rot)] if f2 else [])
    (PESQ / "atracoes-extra.json").write_text(json.dumps(saida, ensure_ascii=False, indent=1), encoding="utf-8")
    (PESQ / "fotos-avulsas.json").write_text(json.dumps(velhas, ensure_ascii=False, indent=1), encoding="utf-8")
    print("antigas com fotos:", len(velhas), "de", len(antigos))
    print("FICARAM DE FORA:"); [print("  ", x) for x in fora]


if __name__ == "__main__":
    main()
