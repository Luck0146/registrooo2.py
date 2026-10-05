# -*- coding: utf-8 -*-
import wx

AUTOR = "Jaquelin Cielo Vidaurre Salazar"
TITULO_APP = "Registro de Negocio"
VERSION_APP = "1.0"

RUBROS = [
    "Abarrotes y Comercio General",
    "Gastronomía y Restauración",
    "Tecnología y Servicios Digitales",
    "Salud, Farmacia y Bienestar",
    "Moda, Calzado y Accesorios",
    "Servicios Técnicos y Mantenimiento",
    "Educación y Capacitación",
    "Otro Rubro Comercial",
]
SERVICIOS = [
    "Envíos a Domicilio / Delivery",
    "Pagos con QR y Tarjeta",
    "Facturación Electrónica",
]
ESTADOS = [
    "Operativo",
    "En Remodelación",
    "Cerrado Temporalmente",
]

TEMAS = {
    "Oscuro": {
        "fondo": "#1b2a4a",
        "panel": "#243456",
        "panel_txt": "#e8eef8",
        "subtitulo": "#9fb4d4",
        "titulo_txt": "#ffffff",
        "campo": "#ffffff",
        "campo_txt": "#1e293b",
        "texto": "#e8eef8",
        "borde": "#0f172a",
        "boton_txt": "#1d4ed8",
        "pie": "#0f172a",
        "pie_txt": "#ffffff",
    },
    "Claro": {
        "fondo": "#f0f4f8",
        "panel": "#ffffff",
        "panel_txt": "#1e293b",
        "subtitulo": "#475569",
        "titulo_txt": "#1b2a4a",
        "campo": "#ffffff",
        "campo_txt": "#1e293b",
        "texto": "#1e293b",
        "borde": "#94a3b8",
        "boton_txt": "#1d4ed8",
        "pie": "#1b2a4a",
        "pie_txt": "#ffffff",
    },
}


def pintar(paneles, textos, campos, opciones, botones, nombre):
    t = TEMAS[nombre]
    for panel in paneles:
        panel.SetBackgroundColour(wx.Colour(t["panel"]))
        if isinstance(panel, wx.StaticBox):
            panel.SetForegroundColour(wx.Colour(t["panel_txt"]))
    for control in textos:
        control.SetForegroundColour(wx.Colour(t["panel_txt"]))
    for control in campos:
        control.SetBackgroundColour(wx.Colour(t["campo"]))
        control.SetForegroundColour(wx.Colour(t["campo_txt"]))
    for control in opciones:
        if isinstance(control, (wx.ComboBox, wx.Choice)):
            control.SetBackgroundColour(wx.Colour(t["campo"]))
            control.SetForegroundColour(wx.Colour(t["campo_txt"]))
        else:
            control.SetForegroundColour(wx.Colour(t["texto"]))
    for control in botones:
        control.SetForegroundColour(wx.Colour(t["boton_txt"]))
        control.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))


class VentanaSecundariaWx(wx.Dialog):
    def __init__(self, parent, tema):
        super().__init__(parent, title="Ventana Secundaria",
                         size=(440, 300), style=wx.DEFAULT_DIALOG_STYLE)

        panel = wx.Panel(self)
        raiz = wx.BoxSizer(wx.VERTICAL)

        titulo = wx.StaticText(panel, label="Bienvenido/a al Sistema de Registro")
        titulo.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        raiz.Add(titulo, 0, wx.ALL | wx.ALIGN_CENTER, 16)

        info = (
            "Información del Sistema\n"
            "----------------------------------------\n"
            "Módulo   : Práctica 1 - Interfaces Gráficas\n"
            "Librería : wxPython %s\n"
            "Versión  : %s\n"
            "Autoría  : %s\n"
            "----------------------------------------"
            % (wx.version(), VERSION_APP, AUTOR)
        )
        self.txt_info = wx.TextCtrl(
            panel, value=info,
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_DONTWRAP
        )
        raiz.Add(self.txt_info, 1, wx.ALL | wx.EXPAND, 12)

        self.btn_cerrar = wx.Button(panel, label="Cerrar")
        self.btn_cerrar.Bind(wx.EVT_BUTTON, self.cerrar_con_confirmacion)

        botones = wx.BoxSizer(wx.HORIZONTAL)
        botones.AddStretchSpacer()
        botones.Add(self.btn_cerrar, 0, wx.ALL, 12)
        raiz.Add(botones, 0, wx.EXPAND)

        panel.SetSizer(raiz)

        self.paneles = [panel]
        self.textos = [titulo]
        self.campos = [self.txt_info]
        self.botones = [self.btn_cerrar]
        pintar(self.paneles, self.textos, self.campos, [], self.botones, tema)

    def cerrar_con_confirmacion(self, evento):
        dialogo = wx.MessageDialog(
            self, "¿Desea cerrar la ventana secundaria?", "Confirmar Cierre",
            wx.YES_NO | wx.ICON_QUESTION
        )
        respuesta = dialogo.ShowModal()
        dialogo.Destroy()
        if respuesta == wx.ID_YES:
            self.EndModal(wx.ID_OK)


class VentanaPrincipalWx(wx.Frame):
    def __init__(self, parent, tema="Oscuro"):
        super().__init__(parent, title="%s - wxPython" % TITULO_APP,
                         size=(880, 720))

        self.total_registros = 0
        self.paneles = []
        self.textos = []
        self.campos = []
        self.opciones = []
        self.botones = []

        self.construir_menu()
        self.construir_interfaz()
        self.actualizar_barra_estado()
        self.aplicar_tema(tema)

    def construir_menu(self):
        archivo = wx.Menu()
        self.id_acerca = archivo.Append(wx.ID_ABOUT, "Acerca de")
        archivo.AppendSeparator()
        self.id_secundaria = archivo.Append(wx.ID_ANY, "Ventana Secundaria")
        archivo.AppendSeparator()
        self.id_salir = archivo.Append(wx.ID_EXIT, "Salir\tCtrl+Q")

        barra = wx.MenuBar()
        barra.Append(archivo, "&Archivo")
        barra.Append(self.crear_menu_ayuda(), "A&yuda")
        self.SetMenuBar(barra)

        self.Bind(wx.EVT_MENU, self.mostrar_acerca_de, self.id_acerca)
        self.Bind(wx.EVT_MENU, self.abrir_ventana_secundaria, self.id_secundaria)
        self.Bind(wx.EVT_MENU, lambda e: self.Close(), self.id_salir)
        self.Bind(wx.EVT_CLOSE, self.cerra_ventana)

    def crear_menu_ayuda(self):
        ayuda = wx.Menu()
        self.id_acerca2 = ayuda.Append(wx.ID_ANY, "Acerca de")
        self.Bind(wx.EVT_MENU, self.mostrar_acerca_de, self.id_acerca2)
        return ayuda

    def construir_interfaz(self):
        self.panel = wx.Panel(self)
        raiz = wx.BoxSizer(wx.VERTICAL)

        self.lbl_titulo = wx.StaticText(self.panel, label=TITULO_APP)
        self.lbl_titulo.SetFont(wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        raiz.Add(self.lbl_titulo, 0, wx.ALL | wx.ALIGN_LEFT, 16)

        self.lbl_subtitulo = wx.StaticText(
            self.panel,
            label="Complete los datos del negocio y presione Registrar / Guardar"
        )
        raiz.Add(self.lbl_subtitulo, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 16)
        self.textos.append(self.lbl_subtitulo)

        raiz.Add(self.construir_formulario(), 0, wx.ALL | wx.EXPAND, 16)
        raiz.Add(self.construir_tema(), 0, wx.LEFT | wx.RIGHT, 16)

        self.lbl_historial = wx.StaticText(
            self.panel, label="Historial de negocios registrados:"
        )
        self.lbl_historial.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        raiz.Add(self.lbl_historial, 0, wx.LEFT | wx.RIGHT | wx.TOP, 16)
        self.textos.append(self.lbl_historial)

        self.txt_historial = wx.TextCtrl(
            self.panel,
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_DONTWRAP | wx.HSCROLL
        )
        raiz.Add(self.txt_historial, 1, wx.ALL | wx.EXPAND, 16)
        self.campos.append(self.txt_historial)

        self.lbl_pie = wx.StaticText(self.panel, label="Autoría: %s" % AUTOR)
        self.lbl_pie.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        raiz.Add(self.lbl_pie, 0, wx.EXPAND)
        self.pie = self.lbl_pie
        self.textos.append(self.lbl_pie)

        self.panel.SetSizer(raiz)
        self.crear_barra_estado()

    def construir_formulario(self):
        grid = wx.FlexGridSizer(cols=2, vgap=10, hgap=12)
        grid.AddGrowableCol(1, 1)

        def etiqueta(texto):
            control = wx.StaticText(self.panel, label=texto)
            self.textos.append(control)
            return control

        grid.Add(etiqueta("Nombre del Negocio:"),
                 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        self.txt_nombre = wx.TextCtrl(self.panel, size=(380, -1))
        grid.Add(self.txt_nombre, 0, wx.EXPAND)
        self.campos.append(self.txt_nombre)

        grid.Add(etiqueta("Propietario / Representante:"),
                 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        self.txt_propietario = wx.TextCtrl(self.panel, size=(380, -1))
        grid.Add(self.txt_propietario, 0, wx.EXPAND)
        self.campos.append(self.txt_propietario)

        grid.Add(etiqueta("Rubro / Categoría:"),
                 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        self.cbo_rubro = wx.ComboBox(self.panel, choices=RUBROS,
                                     style=wx.CB_READONLY, size=(380, -1))
        self.cbo_rubro.SetSelection(0)
        grid.Add(self.cbo_rubro, 0, wx.EXPAND)
        self.opciones.append(self.cbo_rubro)

        grid.Add(etiqueta("Dirección / Ubicación:"),
                 0, wx.ALIGN_LEFT | wx.ALIGN_TOP)
        self.txt_desc = wx.TextCtrl(self.panel, size=(380, 78), style=wx.TE_MULTILINE)
        grid.Add(self.txt_desc, 0, wx.EXPAND)
        self.campos.append(self.txt_desc)

        grid.Add(self.crear_grupo_servicios(), 0, wx.EXPAND)
        grid.AddSpacer(1)
        grid.Add(self.crear_grupo_estado(), 0, wx.EXPAND)
        grid.AddSpacer(1)
        grid.Add(self.crear_fila_botones(), 0, wx.EXPAND)
        grid.AddSpacer(1)

        return grid

    def grupo_horizontal(self, titulo, textos, seleccion_inicial=False):
        caja = wx.StaticBox(self.panel, label=titulo)
        controles = []
        fila = wx.BoxSizer(wx.HORIZONTAL)
        for indice, texto in enumerate(textos):
            if seleccion_inicial:
                control = wx.RadioButton(
                    caja, label=texto, style=wx.RB_GROUP if indice == 0 else 0
                )
            else:
                control = wx.CheckBox(caja, label=texto)
            controles.append(control)
            fila.Add(control, 0, wx.RIGHT, 18)
        fila.AddStretchSpacer()
        marco = wx.StaticBoxSizer(caja, wx.VERTICAL)
        marco.Add(fila, 0, wx.ALL | wx.EXPAND, 10)
        self.paneles.append(caja)
        return marco, controles

    def crear_grupo_servicios(self):
        marco, self.chk_servicios = self.grupo_horizontal(
            "Servicios Habilitados", SERVICIOS
        )
        self.opciones.extend(self.chk_servicios)
        return marco

    def crear_grupo_estado(self):
        marco, self.rdb_estado = self.grupo_horizontal(
            "Estado Comercial Actual", ESTADOS, seleccion_inicial=True
        )
        self.opciones.extend(self.rdb_estado)
        return marco

    def crear_fila_botones(self):
        fila = wx.BoxSizer(wx.HORIZONTAL)
        fila.AddStretchSpacer()

        def boton(texto, manejador):
            control = wx.Button(self.panel, label=texto)
            control.Bind(wx.EVT_BUTTON, manejador)
            self.botones.append(control)
            return control

        fila.Add(boton("Registrar / Guardar", self.registrar), 0, wx.RIGHT, 8)
        fila.Add(boton("Limpiar Formulario", lambda e: self.limpiar()), 0, wx.RIGHT, 8)
        fila.Add(boton("Ventana Secundaria", self.abrir_ventana_secundaria),
                 0, wx.RIGHT, 8)
        fila.Add(boton("Ver Acerca de...", self.mostrar_acerca_de), 0)

        return fila

    def construir_tema(self):
        marco, self.rdb_tema = self.grupo_horizontal(
            "Tema Visual", list(TEMAS), seleccion_inicial=True
        )
        self.opciones.extend(self.rdb_tema)
        for opcion in self.rdb_tema:
            opcion.Bind(wx.EVT_RADIOBUTTON, self.cambiar_tema)
        self.tema_actual = "Oscuro"
        return marco

    def crear_barra_estado(self):
        self.barra_estado = self.CreateStatusBar()
        self.barra_estado.SetStatusText("Listo")

    def cambiar_tema(self, evento):
        self.aplicar_tema(self.rdb_tema[evento.GetSelection()].GetLabel())

    def aplicar_tema(self, nombre):
        self.tema_actual = nombre
        t = TEMAS[nombre]

        self.SetBackgroundColour(wx.Colour(t["fondo"]))
        self.panel.SetBackgroundColour(wx.Colour(t["fondo"]))
        pintar(self.paneles, self.textos, self.campos,
               self.opciones, self.botones, nombre)

        self.lbl_titulo.SetForegroundColour(wx.Colour(t["titulo_txt"]))
        self.lbl_subtitulo.SetForegroundColour(wx.Colour(t["subtitulo"]))
        self.lbl_pie.SetBackgroundColour(wx.Colour(t["pie"]))
        self.lbl_pie.SetForegroundColour(wx.Colour(t["pie_txt"]))
        self.barra_estado.SetBackgroundColour(wx.Colour(t["pie"]))
        self.barra_estado.SetForegroundColour(wx.Colour(t["pie_txt"]))
        self.Refresh()

    def registrar(self, evento):
        nombre = " ".join(self.txt_nombre.GetValue().split())
        propietario = " ".join(self.txt_propietario.GetValue().split())
        descripcion = " ".join(self.txt_desc.GetValue().split())

        faltantes = [
            campo for campo, valor in (
                ("Nombre del Negocio", nombre),
                ("Propietario / Representante", propietario),
                ("Dirección / Ubicación", descripcion),
            ) if not valor
        ]

        if faltantes:
            wx.MessageBox(
                "Complete los siguientes campos obligatorios:\n\n  -  "
                + "\n  -  ".join(faltantes),
                "Campos Incompletos", wx.OK | wx.ICON_WARNING, self
            )
            return

        self.total_registros += 1

        estado = next((r.GetLabel() for r in self.rdb_estado if r.GetValue()),
                      ESTADOS[0])
        servicios = [c.GetLabel() for c in self.chk_servicios if c.GetValue()]

        self.txt_historial.AppendText(
            "Registro #{0:02d}\n"
            "   Negocio      : {1}\n"
            "   Propietario  : {2}\n"
            "   Rubro        : {3}\n"
            "   Dirección    : {4}\n"
            "   Servicios    : {5}\n"
            "   Estado       : {6}\n"
            "   {7}\n\n".format(
                self.total_registros, nombre, propietario,
                self.cbo_rubro.GetStringSelection(),
                descripcion,
                ", ".join(servicios) if servicios else "Sin servicios adicionales",
                estado, "-" * 46
            )
        )

        self.actualizar_barra_estado()
        wx.MessageBox(
            "El negocio '%s' se registró correctamente." % nombre,
            "Registro Exitoso", wx.OK | wx.ICON_INFORMATION, self
        )
        self.limpiar()

    def limpiar(self):
        self.txt_nombre.SetValue("")
        self.txt_propietario.SetValue("")
        self.txt_desc.SetValue("")
        self.cbo_rubro.SetSelection(0)
        for casilla in self.chk_servicios:
            casilla.SetValue(False)
        self.rdb_estado[0].SetValue(True)
        self.txt_nombre.SetFocus()

    def abrir_ventana_secundaria(self, evento):
        dialogo = VentanaSecundariaWx(self, self.tema_actual)
        dialogo.ShowModal()
        dialogo.Destroy()

    def mostrar_acerca_de(self, evento):
        wx.MessageBox(
            "<h3>Registro de Negocio</h3>"
            "<p>Versión %s</p>"
            "<p>Módulo : Práctica 1 - Interfaces Gráficas</p>"
            "<p>Librería : wxPython %s</p>"
            "<p>Autoría : <b>%s</b></p>" % (VERSION_APP, wx.version(), AUTOR),
            "Acerca de", wx.OK | wx.ICON_INFORMATION, self
        )

    def actualizar_barra_estado(self):
        plural = "registro" if self.total_registros == 1 else "registros"
        self.barra_estado.SetStatusText(
            "Total %s: %d  |  Autoría: %s" % (plural, self.total_registros, AUTOR)
        )
        self.SetTitle("%s - wxPython  |  %d %s"
                      % (TITULO_APP, self.total_registros, plural))

    def cerra_ventana(self, evento):
        dialogo = wx.MessageDialog(
            self, "¿Desea salir de la aplicación?", "Confirmar Salida",
            wx.YES_NO | wx.ICON_QUESTION
        )
        respuesta = dialogo.ShowModal()
        dialogo.Destroy()
        if respuesta == wx.ID_YES:
            self.Destroy()
        else:
            evento.Veto()


if __name__ == "__main__":
    app = wx.App(False)
    frame = VentanaPrincipalWx(None, tema="Oscuro")
    frame.Centre()
    frame.Show()
    app.MainLoop()
