from pathlib import Path
import pymupdf as fitz

OUT = Path(__file__).with_name("Manual_Agenda_Clara.pdf")
W, H = 595, 842
REG = r"C:\Windows\Fonts\segoeui.ttf"
BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
GREEN = (35/255, 91/255, 69/255)
INK = (23/255, 37/255, 31/255)
MUTED = (108/255, 121/255, 113/255)
LINE = (226/255, 233/255, 227/255)
PAPER = (1, 1, 1)
BG = (245/255, 247/255, 243/255)
SOFT = (232/255, 241/255, 235/255)
RED = (165/255, 57/255, 52/255)
RED_BG = (1, 241/255, 239/255)
BLUE = (71/255, 123/255, 158/255)
PURPLE = (133/255, 97/255, 157/255)
ORANGE = (198/255, 139/255, 54/255)

doc = fitz.open()

def rect(p, x, y, w, h, fill=PAPER, stroke=LINE, radius=8, sw=0.7):
    p.draw_rect(fitz.Rect(x, y, x+w, y+h), color=stroke, fill=fill, width=sw, radius=min(radius/min(w, h), .45))

def text(p, x, y, s, size=10, color=INK, bold=False):
    p.insert_text((x, y), s, fontsize=size, fontname="fb" if bold else "fr", color=color)

def para(p, box, s, size=10, color=INK, bold=False, align=0, line=1.3):
    return p.insert_textbox(fitz.Rect(*box), s, fontsize=size, fontname="fb" if bold else "fr", color=color, align=align, lineheight=line)

def base(title, kicker, page_no):
    p = doc.new_page(width=W, height=H)
    p.insert_font(fontname="fr", fontfile=REG)
    p.insert_font(fontname="fb", fontfile=BOLD)
    p.draw_rect(fitz.Rect(0, 0, W, H), color=BG, fill=BG)
    p.draw_rect(fitz.Rect(0, 0, W, 9), color=GREEN, fill=GREEN)
    text(p, 38, 39, "AGENDA CLARA  /  MANUAL DO USUÁRIO", 8, GREEN, True)
    text(p, 38, 72, kicker.upper(), 8, MUTED, True)
    para(p, (38, 81, 557, 119), title, 23, INK, True, line=1.05)
    p.draw_line((38, 126), (557, 126), color=LINE, width=0.8)
    p.draw_line((38, 807), (557, 807), color=LINE, width=0.7)
    text(p, 38, 826, "Exemplos fictícios • Nenhum dado da agenda real foi usado", 7.5, MUTED)
    text(p, 525, 826, f"{page_no:02}", 8, GREEN, True)
    return p

def note(p, x, y, w, h, title, body, accent=GREEN):
    rect(p, x, y, w, h, PAPER, LINE, 8)
    p.draw_rect(fitz.Rect(x, y, x+4, y+h), color=accent, fill=accent)
    text(p, x+14, y+20, title, 9, accent, True)
    para(p, (x+14, y+28, x+w-12, y+h-8), body, 8.5, INK, line=1.3)

def pill(p, x, y, s, fill=SOFT, fg=GREEN, w=None):
    if w is None: w=max(50, len(s)*4.4+17)
    rect(p, x, y, w, 19, fill, fill, 8, 0.4)
    para(p, (x+7, y+4, x+w-5, y+16), s, 7, fg, True, line=1)
    return w

def button(p, x, y, w, label, primary=False):
    rect(p,x,y,w,23,GREEN if primary else PAPER,GREEN if primary else LINE,6)
    para(p,(x+5,y+6,x+w-5,y+18),label,7,(1,1,1) if primary else INK,True,1,1)

def checkbox(p,x,y,checked=False,size=12):
    rect(p,x,y,size,size,GREEN if checked else PAPER,GREEN if checked else LINE,2,.7)
    if checked:
        p.draw_line((x+size*.22,y+size*.53),(x+size*.43,y+size*.73),color=PAPER,width=1)
        p.draw_line((x+size*.43,y+size*.73),(x+size*.8,y+size*.28),color=PAPER,width=1)

def field(p,x,y,w,label,value):
    text(p,x,y,label,6.5,MUTED,True)
    rect(p,x,y+4,w,24,PAPER,LINE,5)
    text(p,x+7,y+20,value,7.2,INK)

def browser_frame(p, x, y, w, h, active="Visão geral"):
    rect(p,x,y,w,h,PAPER,LINE,10)
    p.draw_rect(fitz.Rect(x,y,x+w,y+18),color=(239/255,242/255,238/255),fill=(239/255,242/255,238/255))
    for i,c in enumerate((RED,ORANGE,GREEN)): p.draw_circle((x+12+i*10,y+9),2.2,color=c,fill=c)
    para(p,(x+70,y+5,x+w-12,y+13),"agenda-clara.app",6,MUTED,align=1,line=1)
    sx=x+10; sy=y+18; sw=92; sh=h-28
    p.draw_rect(fitz.Rect(sx,sy,sx+sw,sy+sh),color=(249/255,250/255,248/255),fill=(249/255,250/255,248/255))
    text(p,sx+9,sy+18,"agenda clara",8,GREEN,True)
    for i,label in enumerate(("Visão geral","Novo compromisso","Disponibilidade","Relatórios")):
        yy=sy+39+i*25
        if label==active: rect(p,sx+5,yy-12,sw-10,20,SOFT,SOFT,5,0.3)
        text(p,sx+11,yy,label,6.2,GREEN if label==active else MUTED,label==active)
    mx=sx+sw+13; mw=x+w-mx-10
    text(p,mx,sy+17,"AGENDA CLARA  ·  v3.9",6.1,MUTED,True)
    text(p,mx,sy+35,"Seu tempo, mais leve.",12,INK,True)
    button(p,x+w-93,sy+8,78,"Google Calendar",True)
    return mx,sy+48,mw,sh-55

def mini_month(p,x,y,w,month="JUNHO 2026",mark=(5,12,19,24),compact=False):
    step=(10 if w>120 else 7) if compact else 18
    top=4 if compact else 29
    label_y=0 if compact else 10
    day_font=(5 if w>120 else 3.6) if compact else (4.2 if w<120 else 5.3)
    if not compact: text(p,x,y+10,month,7 if w>=120 else 5.2,GREEN,True)
    labels="S T Q Q S S D".split()
    cell=w/7
    for i,l in enumerate(labels):
        if compact: text(p,x+i*cell+cell*.42,y+label_y+11,l,4.2 if w>120 else 3.6,MUTED,True)
        else: para(p,(x+i*cell,y+label_y+7,x+(i+1)*cell,y+label_y+13),l,4.2 if w<120 else 5.5,MUTED,True,1,1)
    # June 2026 starts Monday; Monday-first small grid.
    start=0; days=30
    for d in range(1,days+1):
        col=(start+d-1)%7; row=(start+d-1)//7
        xx=x+col*cell; yy=y+top+row*step
        cellh=(9 if w>120 else 6) if compact else (9 if w<120 else 15)
        if d in mark: rect(p,xx+1,yy,cell-2,cellh,SOFT,(198/255,220/255,205/255),2,0.25)
        if compact: text(p,xx+1,yy+(7 if w>120 else 5),str(d),day_font,GREEN if d in mark else INK,d in mark)
        else: para(p,(xx,yy+1,xx+cell,yy+cellh-1),str(d),day_font,GREEN if d in mark else INK,d in mark,1,1)

def event_row(p,x,y,w,date,time,title,agenda,color=GREEN):
    p.draw_line((x,y),(x+w,y),color=LINE,width=.45)
    text(p,x,y+11,date,6.2,MUTED,True)
    text(p,x,y+22,time,5.7,MUTED)
    p.draw_circle((x+65,y+13),3,color=color,fill=color)
    para(p,(x+73,y+5,x+w-3,y+18),title,7,INK,True,line=1)
    para(p,(x+73,y+19,x+w-3,y+30),agenda,5.7,MUTED,line=1)

# Cover
p=doc.new_page(width=W,height=H); p.insert_font(fontname="fr",fontfile=REG); p.insert_font(fontname="fb",fontfile=BOLD)
p.draw_rect(fitz.Rect(0,0,W,H),color=BG,fill=BG); p.draw_rect(fitz.Rect(0,0,W,12),color=GREEN,fill=GREEN)
text(p,42,54,"AGENDA CLARA",11,GREEN,True); text(p,42,91,"MANUAL DO",10,MUTED,True)
text(p,42,130,"USUÁRIO",34,INK,True)
para(p,(42,153,332,206),"Organize compromissos, consulte disponibilidades e gere relatórios conectados ao Google Calendar.",13,MUTED,line=1.25)
pill(p,42,225,"VERSÃO 3.6",SOFT,GREEN,92); pill(p,142,225,"20/10/2026",PAPER,MUTED,100)
note(p,42,272,244,79,"O QUE ESTE MANUAL MOSTRA","Passo a passo para cadastrar, consultar, conciliar agendas e imprimir relatórios. As telas são ilustrações da interface com exemplos inventados.")
# Large illustrative screen
mx,my,mw,mh=browser_frame(p,42,385,511,290)
rect(p,mx,my,mw,mh,PAPER,LINE,8)
text(p,mx+12,my+20,"Bom dia",12,INK,True)
text(p,mx+12,my+35,"Visão geral da agenda e atalhos principais",6.5,MUTED)
# card left
cw=(mw-34)/2
rect(p,mx+10,my+50,cw,143,PAPER,LINE,7)
text(p,mx+20,my+67,"Agenda próxima",8.5,INK,True)
pill(p,mx+20,my+73,"3 COMPROMISSOS",SOFT,GREEN,91)
event_row(p,mx+20,my+99,cw-20,"Hoje","10:00–11:00","Reunião de planejamento","Trabalho",GREEN)
event_row(p,mx+20,my+132,cw-20,"Amanhã","14:00–15:00","Revisar material","Universidade",PURPLE)
# right card
rect(p,mx+cw+24,my+50,cw,143,PAPER,LINE,7)
text(p,mx+cw+34,my+67,"Consulta rápida",8.5,INK,True)
text(p,mx+cw+34,my+82,"Período: junho a julho",6.3,MUTED)
for i,label in enumerate(("sex. 05 a dom. 07  ·  Livre","sex. 12 a dom. 14  ·  Ocupado")):
    yy=my+94+i*30; col=RED if i else GREEN; fill=RED_BG if i else SOFT
    rect(p,mx+cw+34,yy,cw-20,23,fill,fill,5,0.2)
    text(p,mx+cw+42,yy+15,label,6.2,col,True)
rect(p,mx+10,my+202,mw-20,55,SOFT,SOFT,7)
text(p,mx+21,my+222,"Atalhos",8,GREEN,True)
text(p,mx+21,my+239,"Novo compromisso  ·  Relatório  ·  Conciliação  ·  Tema escuro",7,INK)
note(p,42,711,511,64,"DADOS DE EXEMPLO","“Reunião de planejamento”, “Trabalho” e os horários deste manual são fictícios. Nenhuma captura usa sua agenda real.",GREEN)
text(p,42,799,"Acesso pelo navegador no computador ou celular",8,MUTED)

# Page 2: Navigation and main screen
p=base("Conheça a tela inicial","01 · Visão geral",2)
para(p,(38,141,550,174),"Ao abrir o app, a Consulta rápida mostra a partir do mês atual e avança dois meses. Os demais cartões podem permanecer ocultos até você precisar deles.",10,MUTED)
mx,my,mw,mh=browser_frame(p,38,188,519,302)
rect(p,mx,my,mw,mh,PAPER,LINE,8)
text(p,mx+12,my+20,"Bom dia",12,INK,True)
text(p,mx+12,my+36,"Resumo da semana",6.4,MUTED)
cw=(mw-34)/2
rect(p,mx+10,my+50,cw,154,PAPER,LINE,7)
text(p,mx+20,my+68,"Agenda próxima",8.5,INK,True)
event_row(p,mx+20,my+80,cw-20,"Hoje","10:00–11:00","Reunião de planejamento","Trabalho",GREEN)
event_row(p,mx+20,my+114,cw-20,"Amanhã","12:00–13:00","Almoço","Pessoal",BLUE)
event_row(p,mx+20,my+148,cw-20,"Quinta","14:00–15:00","Orientação de projeto","Universidade",PURPLE)
rect(p,mx+cw+24,my+50,cw,154,PAPER,LINE,7)
text(p,mx+cw+34,my+68,"Consulta rápida",8.5,INK,True)
text(p,mx+cw+34,my+82,"Junho – julho de 2026",6.3,MUTED)
rect(p,mx+cw+34,my+94,cw-20,29,SOFT,SOFT,5,.2); text(p,mx+cw+42,my+112,"05 a 07 jun.  ·  Livre",6.5,GREEN,True)
rect(p,mx+cw+34,my+129,cw-20,29,RED_BG,RED_BG,5,.2); text(p,mx+cw+42,my+147,"12 a 14 jun.  ·  Ocupado",6.5,RED,True)
text(p,mx+cw+34,my+178,"Ver dias e horários livres",6.1,MUTED)
note(p,38,512,248,101,"ABRIR O GOOGLE CALENDAR","Use o botão verde no topo para abrir sua agenda Google em outra página. O app continua aberto.")
note(p,300,512,257,101,"NAVEGAR PELO APP","Os botões Visão geral, Novo compromisso, Disponibilidade e Relatórios levam às áreas principais.",BLUE)
note(p,38,626,248,101,"OCULTAR CARTÕES","Use o ícone Cartões para escolher o que aparece. Ao ocultar, a grade se reorganiza automaticamente.",PURPLE)
note(p,300,626,257,101,"TEMA ESCURO","O botão Tema alterna a aparência. A preferência fica salva neste navegador.",GREEN)
para(p,(38,747,557,789),"Dica: no celular, use os mesmos cartões e controles. Para acesso rápido, abra a URL no navegador e adicione o app à tela inicial.",9,MUTED)

# Page 3: New event form
p=base("Cadastrar um compromisso","02 · Novo compromisso",3)
para(p,(38,141,552,172),"Preencha o essencial: título, categoria, agenda, data e horário. A prévia abaixo da data mostra compromissos já marcados naquele dia.",10,MUTED)
rect(p,38,185,321,385,PAPER,LINE,10)
text(p,55,210,"Novo compromisso",12,INK,True); text(p,55,226,"Preencha o essencial e pronto.",7,MUTED)
pill(p,55,240,"COMPROMISSO",SOFT,GREEN,104); pill(p,166,240,"LEMBRETE",PAPER,MUTED,83)
text(p,55,280,"O que você precisa fazer?",7,MUTED,True); rect(p,55,288,287,29,PAPER,LINE,6); text(p,64,306,"Preparar apresentação",8,INK)
text(p,55,337,"Categoria",7,MUTED,True); rect(p,55,345,132,28,PAPER,LINE,6); text(p,64,363,"Profissional  ▾",7,INK)
text(p,199,337,"Adicionar em qual agenda?",7,MUTED,True); rect(p,199,345,143,28,PAPER,LINE,6); text(p,207,363,"Trabalho  ▾",7,INK)
text(p,55,394,"Data",7,MUTED,True); rect(p,55,402,132,28,PAPER,LINE,6); text(p,64,420,"10/06/2026",7,INK)
text(p,199,394,"Horário",7,MUTED,True); rect(p,199,402,143,28,PAPER,LINE,6); text(p,207,420,"09:00 – 10:00",7,INK)
rect(p,55,440,287,22,SOFT,SOFT,5,.3); checkbox(p,64,445,False,11); text(p,81,455,"Dia todo",7,GREEN,True)
rect(p,55,469,287,48,(249/255,250/255,248/255),LINE,6); text(p,64,486,"1 compromisso já existe nesta data",6.7,INK,True); text(p,64,502,"Universidade · Orientação de projeto · 14:00–15:00",6,MUTED)
button(p,55,529,287,"Adicionar à agenda",True)
note(p,378,188,179,89,"COMPROMISSOS PRONTOS","Coordenação Ebpos e Aula XXX preenchem título e agenda de destino.",PURPLE)
note(p,378,289,179,90,"LEMBRETES PRONTOS","Preparar apresentação, Subir conteúdo e Avaliar a turma agilizam o preenchimento.",BLUE)
note(p,378,391,179,91,"DIA TODO E ALERTA","Marque Dia todo quando não houver horário específico. O alerta pop-up do Google Calendar pode ser ativado no cadastro.",GREEN)
note(p,378,494,179,91,"PRÉVIA DE CONFLITOS","A lista embaixo da data atualiza com os itens existentes. Confira o horário antes de salvar.",ORANGE)
note(p,38,598,519,99,"EXEMPLO FICTÍCIO","Título: Preparar apresentação · Categoria: Profissional · Agenda: Trabalho · Data: 10/06/2026 · Horário: 09:00–10:00 · Alerta: 30 minutos antes. Esses valores ilustram o preenchimento; não são eventos reais.")
para(p,(38,716,552,777),"Depois de adicionar, o compromisso é gravado na agenda selecionada do Google Calendar. A categoria ajuda a identificar o tipo de atividade; a agenda determina onde o evento será armazenado.",9,MUTED)

# Page 4: Quick availability
p=base("Consultar disponibilidade","03 · Consulta rápida",4)
para(p,(38,141,557,177),"Escolha o mês inicial e final, as agendas que entram na consulta e o formato: horários livres, dia inteiro ou fins de semana.",10,MUTED)
rect(p,38,189,519,308,PAPER,LINE,10)
text(p,55,215,"Consulta rápida",12,INK,True); text(p,55,231,"Encontre um horário livre.",7,MUTED)
field(p,55,249,166,"Mês inicial","junho de 2026"); field(p,233,249,166,"Mês final","julho de 2026")
field(p,55,291,205,"Duração","1 hora  ▾")
checkbox(p,275,300,True,13); text(p,296,311,"Fins de semana",7,INK)
checkbox(p,55,333,True,13); text(p,76,344,"Procurar dias totalmente livres",7,INK)
button(p,55,359,466,"Ver dias e horários livres",False)
rect(p,55,397,466,35,SOFT,SOFT,6,.2); text(p,67,419,"sex., 05 jun. a dom., 07 jun.",7,INK); text(p,442,419,"Fim de semana livre",7,GREEN,True)
rect(p,55,439,466,43,RED_BG,(1,.72,.7),6,.4); text(p,67,457,"sex., 12 jun. a dom., 14 jun.",7,RED,True); text(p,448,457,"Ocupado",7,RED,True); text(p,67,474,"Observação: Trabalho · Projeto Alfa (dia todo)",6.5,RED)
note(p,38,520,250,92,"FINS DE SEMANA","Quando marcado, a consulta agrupa sexta, sábado e domingo como um bloco de dia todo. Se qualquer dia tiver conflito, o bloco fica vermelho.",GREEN)
note(p,300,520,257,92,"AGENDAS SELECIONADAS","Abra o seletor Agendas para escolher uma, várias ou todas. A disponibilidade considera as agendas escolhidas.",PURPLE)
text(p,38,647,"COPIAR PARA WHATSAPP",8,GREEN,True)
rect(p,38,658,519,95,PAPER,LINE,8)
para(p,(53,674,541,726),"junho de 2026  ·  05 a 07 de junho  ·  19 a 21 de junho\njulho de 2026  ·  03 a 05 de julho",8.5,INK,line=1.35)
button(p,385,715,155,"Copiar disponibilidade",True)
para(p,(38,768,557,795),"A cópia inclui os intervalos livres e, se você marcar a caixa ao lado de um fim de semana ocupado, inclui esse bloco no mesmo padrão. O app copia o texto; você decide para quem enviar.",8,MUTED)

# Page 5: Conflicts and filtering
p=base("Filtrar agendas e conciliar","04 · Agendas e conflitos",5)
para(p,(38,141,557,174),"A Consulta rápida, a Agenda próxima, o relatório e a Conciliação têm seleção de agendas. Escolha quais calendários entram em cada visão.",10,MUTED)
rect(p,38,185,519,244,PAPER,LINE,10)
text(p,55,211,"Conciliação",12,INK,True); text(p,55,229,"Encontre sobreposições entre agendas diferentes.",7,MUTED)
pill(p,55,242,"2 CONFLITOS",RED_BG,RED,91)
for yy,date,title1,agenda1,time1,title2,agenda2,time2 in [
    (279,"qua., 10 jun. · horários sobrepostos","Reunião de projeto","Trabalho","10:00–11:00","Orientação de projeto","Universidade","10:30–11:30"),
    (350,"sex., 19 jun. · horários sobrepostos","Revisão de material","Trabalho","14:00–15:00","Reunião de equipe","Universidade","14:30–15:30")]:
    rect(p,55,yy,485,62,RED_BG,(1,.77,.75),6,.4); text(p,66,yy+15,date,6.8,RED,True)
    p.draw_circle((71,yy+31),3,color=GREEN,fill=GREEN); text(p,81,yy+34,f"{agenda1}: {title1} ({time1})",6.2,INK)
    p.draw_circle((71,yy+47),3,color=PURPLE,fill=PURPLE); text(p,81,yy+50,f"{agenda2}: {title2} ({time2})",6.2,INK)
note(p,38,456,250,88,"NOME E COR","Cada item mostra a agenda de origem e sua cor, para identificar rapidamente de onde vem cada compromisso.",GREEN)
note(p,300,456,257,88,"FILTRO DA CONCILIAÇÃO","Abra Agendas no cartão Conciliação e marque os calendários que quer comparar. Só há conflito quando horários se sobrepõem em agendas diferentes.",PURPLE)
text(p,38,579,"EXEMPLO DE SELEÇÃO",8,GREEN,True)
rect(p,38,591,519,117,PAPER,LINE,8)
for i,(name,col,checked) in enumerate((("Trabalho",GREEN,True),("Universidade",PURPLE,True),("Pessoal",BLUE,False))):
    yy=612+i*26; checkbox(p,55,yy-10,checked,12)
    p.draw_circle((81,yy-4),4,color=col,fill=col); text(p,93,yy,name,8,INK)
para(p,(270,608,540,689),"Neste exemplo fictício, a Conciliação compara Trabalho e Universidade. Pessoal está desmarcada, então seus eventos não entram na busca de conflitos.",8.5,MUTED,line=1.3)
note(p,38,731,519,52,"DICA","Use o filtro para investigar uma combinação específica de agendas. Reative todas para revisar a visão completa.",ORANGE)

# Page 6: Reports and print
p=base("Gerar e imprimir relatórios","05 · Relatórios",6)
para(p,(38,141,557,174),"O relatório pode cobrir um mês ou um intervalo personalizado. Filtre as agendas, gere o resumo e use PDF / imprimir.",10,MUTED)
rect(p,38,187,519,245,PAPER,LINE,10)
text(p,55,213,"Relatório do período",12,INK,True)
pill(p,55,223,"MÊS",SOFT,GREEN,54); pill(p,114,223,"PERSONALIZADO",PAPER,MUTED,101)
field(p,55,257,170,"Mês","junho de 2026")
button(p,55,302,202,"Gerar resumo",False); button(p,269,302,202,"PDF / imprimir",True)
text(p,55,347,"12 compromissos · 3 pessoais · 4 universitários · 5 profissionais",7,INK,True)
text(p,55,368,"Junho de 2026",8,GREEN,True)
mini_month(p,55,376,156,"JUNHO 2026",(3,5,10,12,19,24),compact=True)
text(p,248,375,"COMPROMISSOS",6.5,MUTED,True)
for i,(d,title,ag,col) in enumerate((("03 jun. · 09:00","Reunião de planejamento","Trabalho",GREEN),("10 jun. · 10:30","Orientação de projeto","Universidade",PURPLE),("19 jun. · Dia todo","Projeto Alfa","Trabalho",GREEN))):
    yy=389+i*14; p.draw_circle((253,yy-2),2.5,color=col,fill=col); text(p,261,yy,title,6.4,INK,True); text(p,261,yy+8,f"{d} · {ag}",5.5,MUTED)
text(p,38,469,"FORMATO DA IMPRESSÃO",8,GREEN,True)
# 2 page thumbnails
rect(p,38,482,248,214,PAPER,LINE,8)
text(p,52,501,"PÁGINA 1 · MINI CALENDÁRIOS",7,GREEN,True)
text(p,52,514,"Visão geral de todos os meses incluídos",6,MUTED)
for i,m in enumerate(("JUNHO 2026","JULHO 2026","AGOSTO 2026")):
    xx=52+(i%2)*108; yy=530+(i//2)*78
    rect(p,xx,yy,98,66,(249/255,250/255,248/255),LINE,5,.3)
    mini_month(p,xx+5,yy+5,87,m,(3,10,19,24))
rect(p,300,482,257,214,PAPER,LINE,8)
text(p,314,501,"PÁGINA 2+ · DETALHES",7,GREEN,True)
text(p,314,514,"Calendário e lista do mês juntos, em duas colunas",6,MUTED)
for i,(xx,yy,month,events) in enumerate(((314,530,"JUNHO 2026",("Reunião · Trabalho","Orientação · Universidade")),(434,530,"JULHO 2026",("Revisão · Trabalho","Aula · Universidade")),(314,615,"AGOSTO 2026",("Planejamento · Trabalho",)))):
    rect(p,xx,yy,108,77,(249/255,250/255,248/255),LINE,5,.3)
    text(p,xx+5,yy+11,month,5,GREEN,True)
    mini_month(p,xx+5,yy+14,43,month,(3,10,19,24),compact=True)
    text(p,xx+52,yy+20,"Compromissos",4.8,GREEN,True)
    for j,label in enumerate(events):
        p.draw_circle((xx+55,yy+30+j*11),1.5,color=GREEN if j==0 else PURPLE,fill=GREEN if j==0 else PURPLE)
        para(p,(xx+59,yy+25+j*11,xx+105,yy+36+j*11),label,4.3,INK,line=1)
note(p,38,711,519,70,"DICA DE IMPRESSÃO","Na impressão, selecione A4. A primeira página mostra somente os mini calendários em duas colunas e em ordem cronológica. Depois, cada mês ocupa uma página própria, com o mini calendário no topo e os compromissos em duas colunas.",BLUE)

# Page 7: Mobile use and privacy
p=base("Usar no celular e manter seus dados protegidos","06 · Celular e boas práticas",7)
para(p,(38,141,557,174),"O layout se adapta a telas pequenas. Abra a mesma URL no navegador do celular e, se quiser, adicione à tela inicial.",10,MUTED)
# phone mock
rect(p,48,188,205,417,(32/255,42/255,36/255),(32/255,42/255,36/255),23,1)
rect(p,57,204,187,383,BG,BG,17,.4)
rect(p,114,210,72,8,(32/255,42/255,36/255),(32/255,42/255,36/255),5,.3)
text(p,70,241,"agenda clara",10,GREEN,True); text(p,70,263,"Seu tempo, mais leve.",10,INK,True)
rect(p,68,275,165,96,PAPER,LINE,10)
text(p,79,294,"Consulta rápida",9,INK,True); text(p,79,309,"Junho a julho de 2026",6,MUTED)
rect(p,79,319,143,20,SOFT,SOFT,5,.2); text(p,86,333,"05 a 07 jun. · Livre",6,GREEN,True)
rect(p,79,344,143,20,RED_BG,RED_BG,5,.2); text(p,86,358,"12 a 14 jun. · Ocupado",6,RED,True)
rect(p,68,380,165,94,PAPER,LINE,10)
text(p,79,399,"Novo compromisso",9,INK,True); text(p,79,416,"Preparar apresentação",6,INK)
text(p,79,431,"Trabalho · 09:00–10:00",5.8,MUTED); button(p,79,441,143,"Adicionar",True)
rect(p,68,483,165,85,PAPER,LINE,10)
text(p,79,502,"Agenda próxima",9,INK,True); text(p,79,519,"10:00 · Reunião de planejamento",5.6,INK); text(p,79,537,"14:00 · Revisar material",5.6,INK)
note(p,285,194,272,82,"ACESSO NO CELULAR","Abra o link no navegador do aparelho. No menu do navegador, escolha Adicionar à tela inicial para criar um atalho.",GREEN)
note(p,285,287,272,82,"PERMISSÃO DO GOOGLE","O Apps Script pede acesso ao Calendar para consultar e criar eventos. Use a conta correta e revise a permissão exibida pelo Google.",PURPLE)
note(p,285,380,272,82,"EXEMPLOS ANONIMIZADOS","Os nomes, horários e agendas usados nas telas deste manual são fictícios. Substitua pelos seus dados ao usar o app.",BLUE)
note(p,285,473,272,82,"COMPARTILHAMENTO","A cópia para WhatsApp fica no clipboard do aparelho. Revise o texto e escolha manualmente a conversa antes de enviar.",ORANGE)
text(p,38,643,"LEMBRETES RÁPIDOS",8,GREEN,True)
note(p,38,655,250,99,"PREPARAR APRESENTAÇÃO","Toque no lembrete pronto, confirme o título e a agenda, escolha data e horário e salve.",PURPLE)
note(p,300,655,257,99,"SUBIR CONTEÚDO / AVALIAR","Os lembretes preenchem o título. Você pode editar detalhes antes de adicionar ao Calendar.",GREEN)
para(p,(38,773,557,799),"Versão deste manual: Agenda Clara v3.9 · 20/10/2026",8,MUTED)

doc.set_metadata({"title":"Manual do usuário — Agenda Clara","author":"Agenda Clara","subject":"Guia de uso com exemplos fictícios e telas ilustrativas"})
doc.save(OUT, garbage=4, deflate=True)
print(OUT)
