"""
view/__init__.py
GUI completa do Sistema Acadêmico usando CustomTkinter.
"""
from __future__ import annotations

import customtkinter as ctk
from tkinter import messagebox

from security import Role, User
from repository import PersistenceType
from controller import AcademicSystemController
from exceptions import (
    AuthenticationException,
    AcademicDomainException,
    AuthorizationException,
    AccessDeniedException,
    InvalidAssessmentException,
)

# ── Tema global ─────────────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ── Paleta de cores ──────────────────────────────────────────────────────────
C_BG        = "#1e1e2e"   # fundo principal
C_SURFACE   = "#2a2a3e"   # painéis / cards
C_ACCENT    = "#7c6af7"   # roxo primário
C_ACCENT2   = "#5c9cf7"   # azul secundário
C_SUCCESS   = "#4caf76"
C_ERROR     = "#cf4f4f"
C_TEXT      = "#e0e0f0"
C_MUTED     = "#9090b0"

FONT_TITLE  = ("Segoe UI", 22, "bold")
FONT_SUB    = ("Segoe UI", 14, "bold")
FONT_BODY   = ("Segoe UI", 12)
FONT_SMALL  = ("Segoe UI", 10)
FONT_MONO   = ("Consolas", 11)


# ── Helper widgets ───────────────────────────────────────────────────────────

def _label(parent, text, font=FONT_BODY, text_color=C_TEXT, **kw):
    return ctk.CTkLabel(parent, text=text, font=font, text_color=text_color, **kw)


def _entry(parent, placeholder="", show="", **kw):
    return ctk.CTkEntry(
        parent, placeholder_text=placeholder, show=show,
        fg_color=C_SURFACE, border_color=C_ACCENT, text_color=C_TEXT,
        font=FONT_BODY, height=38, **kw
    )


def _btn(parent, text, command, color=C_ACCENT, hover=None, width=200, **kw):
    return ctk.CTkButton(
        parent, text=text, command=command,
        fg_color=color, hover_color=hover or C_ACCENT2,
        text_color="white", font=("Segoe UI", 13, "bold"),
        corner_radius=10, height=40, width=width, **kw
    )


def _card(parent, **kw):
    return ctk.CTkFrame(parent, fg_color=C_SURFACE, corner_radius=12, **kw)


def _textarea(parent, height=200, **kw):
    return ctk.CTkTextbox(
        parent, height=height, fg_color=C_SURFACE,
        text_color=C_TEXT, font=FONT_MONO,
        border_color=C_ACCENT, border_width=1, **kw
    )


def _msg_label(parent):
    lbl = ctk.CTkLabel(parent, text="", font=FONT_SMALL, text_color=C_SUCCESS)
    return lbl


def _set_msg(lbl, text, success=True):
    lbl.configure(text=text, text_color=C_SUCCESS if success else C_ERROR)


# ── Tela de Login ────────────────────────────────────────────────────────────

class LoginScreen(ctk.CTkFrame):
    def __init__(self, master, controller: AcademicSystemController, on_success):
        super().__init__(master, fg_color=C_BG)
        self._controller = controller
        self._on_success = on_success
        self._build()

    def _build(self):
        self.pack(fill="both", expand=True)

        # centro vertical
        center = ctk.CTkFrame(self, fg_color=C_BG)
        center.place(relx=0.5, rely=0.5, anchor="center")

        # logo / título
        _label(center, "🎓 Sistema Acadêmico", font=FONT_TITLE, text_color=C_ACCENT).pack(pady=(0, 6))
        _label(center, "Faça login para continuar", font=FONT_BODY, text_color=C_MUTED).pack(pady=(0, 30))

        card = _card(center)
        card.pack(padx=20, pady=10, ipadx=30, ipady=30)

        _label(card, "Usuário", font=("Segoe UI", 11)).pack(anchor="w", padx=10, pady=(10, 0))
        self._txt_user = _entry(card, placeholder="ex: admin", width=300)
        self._txt_user.pack(padx=10, pady=4)

        _label(card, "Senha", font=("Segoe UI", 11)).pack(anchor="w", padx=10, pady=(10, 0))
        self._txt_pass = _entry(card, placeholder="senha", show="•", width=300)
        self._txt_pass.pack(padx=10, pady=4)

        self._lbl_err = ctk.CTkLabel(card, text="", font=FONT_SMALL, text_color=C_ERROR)
        self._lbl_err.pack(pady=(6, 0))

        btn = _btn(card, "Entrar", self._login, width=300)
        btn.pack(padx=10, pady=(12, 10))

        # dica de credenciais
        hint = _card(center)
        hint.pack(pady=(16, 0), padx=20, fill="x")
        _label(hint, "Credenciais padrão:", font=("Segoe UI", 10, "bold"), text_color=C_MUTED).pack(anchor="w", padx=10, pady=(8, 2))
        _label(hint, "  admin / admin123   (ADMIN)", font=FONT_SMALL, text_color=C_MUTED).pack(anchor="w", padx=10)
        _label(hint, "  professor / prof123   (PROFESSOR)", font=FONT_SMALL, text_color=C_MUTED).pack(anchor="w", padx=10, pady=(0, 8))

        # bind Enter
        self._txt_pass.bind("<Return>", lambda e: self._login())
        self._txt_user.bind("<Return>", lambda e: self._txt_pass.focus())

    def _login(self):
        self._lbl_err.configure(text="")
        try:
            self._controller.login(self._txt_user.get(), self._txt_pass.get())
            user = self._controller.get_authenticated_user()
            self._on_success(user)
        except AuthenticationException as ex:
            self._lbl_err.configure(text=str(ex))


# ── Tela Principal (menu lateral) ────────────────────────────────────────────

class MainScreen(ctk.CTkFrame):
    def __init__(self, master, controller: AcademicSystemController, user: User, on_logout):
        super().__init__(master, fg_color=C_BG)
        self._controller = controller
        self._user = user
        self._on_logout = on_logout
        self._build()

    def _build(self):
        self.pack(fill="both", expand=True)

        # ── Sidebar ────────────────────────────────────────────────────────
        sidebar = ctk.CTkFrame(self, width=230, fg_color=C_SURFACE, corner_radius=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        _label(sidebar, "🎓 Acadêmico", font=("Segoe UI", 16, "bold"), text_color=C_ACCENT).pack(pady=(24, 4))
        _label(sidebar, f"Olá, {self._user.username}", font=FONT_BODY, text_color=C_TEXT).pack()
        role_color = C_ACCENT if self._user.role == Role.ADMIN else C_ACCENT2
        _label(sidebar, f"[{self._user.role.value}]", font=FONT_SMALL, text_color=role_color).pack(pady=(0, 20))

        ctk.CTkFrame(sidebar, height=1, fg_color=C_MUTED).pack(fill="x", padx=16, pady=8)

        # ── Content area ────────────────────────────────────────────────────
        self._content = ctk.CTkFrame(self, fg_color=C_BG)
        self._content.pack(side="right", fill="both", expand=True)

        # menu items
        is_admin = self._user.role == Role.ADMIN

        def nav(text, icon, screen_fn, allowed=True):
            if not allowed:
                return
            btn = ctk.CTkButton(
                sidebar, text=f"  {icon}  {text}", anchor="w",
                fg_color="transparent", hover_color=C_BG,
                text_color=C_TEXT, font=FONT_BODY,
                height=40, corner_radius=8, command=screen_fn,
            )
            btn.pack(fill="x", padx=12, pady=2)

        nav("Dashboard",           "📊", self._show_dashboard)
        nav("Cadastrar Turma",     "📋", self._show_class_reg, is_admin)
        nav("Cadastrar Avaliação", "✏️", self._show_assessment_reg)
        nav("Turmas e Avaliações", "📂", self._show_visualization)
        nav("Relatórios",          "📄", self._show_reports)
        nav("Persistência",        "💾", self._show_persistence, is_admin)
        nav("Salvar Dados",        "🗸",  self._save_data, is_admin)

        ctk.CTkFrame(sidebar, height=1, fg_color=C_MUTED).pack(fill="x", padx=16, pady=16)

        ctk.CTkButton(
            sidebar, text="  🚪  Logout", anchor="w",
            fg_color="transparent", hover_color=C_ERROR,
            text_color=C_ERROR, font=FONT_BODY,
            height=40, corner_radius=8, command=self._logout,
        ).pack(fill="x", padx=12, pady=2)

        self._show_dashboard()

    def _clear_content(self):
        for w in self._content.winfo_children():
            w.destroy()

    def _show_dashboard(self):
        self._clear_content()
        DashboardPanel(self._content, self._controller, self._user)

    def _show_class_reg(self):
        self._clear_content()
        ClassRegistrationPanel(self._content, self._controller)

    def _show_assessment_reg(self):
        self._clear_content()
        AssessmentRegistrationPanel(self._content, self._controller)

    def _show_visualization(self):
        self._clear_content()
        VisualizationPanel(self._content, self._controller)

    def _show_reports(self):
        self._clear_content()
        ReportPanel(self._content, self._controller, self._user)

    def _show_persistence(self):
        self._clear_content()
        PersistencePanel(self._content, self._controller)

    def _save_data(self):
        try:
            result = self._controller.save_academic_data()
            messagebox.showinfo("Sucesso", result)
        except (AcademicDomainException, AccessDeniedException, Exception) as ex:
            messagebox.showerror("Erro", str(ex))

    def _logout(self):
        self._controller.logout()
        self._on_logout()


# ── Dashboard ────────────────────────────────────────────────────────────────

class DashboardPanel(ctk.CTkFrame):
    def __init__(self, master, controller: AcademicSystemController, user: User):
        super().__init__(master, fg_color=C_BG)
        self.pack(fill="both", expand=True, padx=24, pady=24)
        self._controller = controller
        self._user = user
        self._build()

    def _build(self):
        _label(self, "Dashboard", font=FONT_TITLE, text_color=C_ACCENT).pack(anchor="w", pady=(0, 20))

        # Status card
        cards_row = ctk.CTkFrame(self, fg_color=C_BG)
        cards_row.pack(fill="x", pady=(0, 16))

        try:
            status = self._controller.get_system_status()
        except Exception:
            status = "Sistema em execução."

        classes = self._controller._class_service.list_classes()
        total_classes = len(classes)
        total_assessments = sum(len(c.assessments) for c in classes)
        pt = self._controller.get_current_persistence_type()

        self._stat_card(cards_row, "🏫", "Turmas", str(total_classes), C_ACCENT)
        self._stat_card(cards_row, "✏️", "Avaliações", str(total_assessments), C_ACCENT2)
        self._stat_card(cards_row, "💾", "Persistência", pt.description, C_SUCCESS)

        # Info card
        info = _card(self)
        info.pack(fill="x", pady=8)
        _label(info, "Informações do Sistema", font=FONT_SUB, text_color=C_ACCENT).pack(anchor="w", padx=16, pady=(12, 4))
        _label(info, status, font=FONT_BODY, text_color=C_TEXT).pack(anchor="w", padx=16, pady=(0, 12))

    def _stat_card(self, parent, icon, label, value, color):
        card = _card(parent)
        card.pack(side="left", padx=8, pady=4, ipadx=16, ipady=12, fill="x", expand=True)
        _label(card, icon, font=("Segoe UI", 24)).pack()
        _label(card, value, font=("Segoe UI", 22, "bold"), text_color=color).pack()
        _label(card, label, font=FONT_SMALL, text_color=C_MUTED).pack()


# ── Cadastro de Turmas ───────────────────────────────────────────────────────

class ClassRegistrationPanel(ctk.CTkFrame):
    def __init__(self, master, controller: AcademicSystemController):
        super().__init__(master, fg_color=C_BG)
        self.pack(fill="both", expand=True, padx=24, pady=24)
        self._controller = controller
        self._build()

    def _build(self):
        _label(self, "Cadastrar Turma", font=FONT_TITLE, text_color=C_ACCENT).pack(anchor="w", pady=(0, 20))

        card = _card(self)
        card.pack(fill="x", pady=8, ipadx=20, ipady=20)

        _label(card, "Código da Turma *", font=FONT_BODY).pack(anchor="w", padx=16, pady=(16, 2))
        self._txt_code = _entry(card, placeholder="ex: CS101", width=400)
        self._txt_code.pack(anchor="w", padx=16, pady=(0, 10))

        _label(card, "Nome da Turma *", font=FONT_BODY).pack(anchor="w", padx=16, pady=(0, 2))
        self._txt_name = _entry(card, placeholder="ex: Programação Orientada a Objetos", width=400)
        self._txt_name.pack(anchor="w", padx=16, pady=(0, 10))

        self._lbl_msg = _msg_label(card)
        self._lbl_msg.pack(anchor="w", padx=16)

        _btn(card, "✅  Cadastrar Turma", self._register_class, width=220).pack(anchor="w", padx=16, pady=(10, 16))

    def _register_class(self):
        _set_msg(self._lbl_msg, "")
        try:
            msg = self._controller.register_class(self._txt_code.get(), self._txt_name.get())
            _set_msg(self._lbl_msg, msg, success=True)
            self._txt_code.delete(0, "end")
            self._txt_name.delete(0, "end")
        except Exception as ex:
            _set_msg(self._lbl_msg, str(ex), success=False)


# ── Cadastro de Avaliações ────────────────────────────────────────────────────

class AssessmentRegistrationPanel(ctk.CTkFrame):
    def __init__(self, master, controller: AcademicSystemController):
        super().__init__(master, fg_color=C_BG)
        self.pack(fill="both", expand=True, padx=24, pady=24)
        self._controller = controller
        self._build()

    def _build(self):
        _label(self, "Cadastrar Avaliação", font=FONT_TITLE, text_color=C_ACCENT).pack(anchor="w", pady=(0, 20))

        card = _card(self)
        card.pack(fill="x", pady=8, ipadx=20, ipady=20)

        _label(card, "Código da Turma *", font=FONT_BODY).pack(anchor="w", padx=16, pady=(16, 2))
        self._txt_class = _entry(card, placeholder="ex: CS101", width=400)
        self._txt_class.pack(anchor="w", padx=16, pady=(0, 10))

        _label(card, "Nome da Avaliação *", font=FONT_BODY).pack(anchor="w", padx=16, pady=(0, 2))
        self._txt_name = _entry(card, placeholder="ex: Prova 1", width=400)
        self._txt_name.pack(anchor="w", padx=16, pady=(0, 10))

        _label(card, "Peso (0.0 – 1.0) *", font=FONT_BODY).pack(anchor="w", padx=16, pady=(0, 2))
        self._txt_weight = _entry(card, placeholder="ex: 0.40", width=200)
        self._txt_weight.pack(anchor="w", padx=16, pady=(0, 10))

        self._lbl_msg = _msg_label(card)
        self._lbl_msg.pack(anchor="w", padx=16)

        _btn(card, "✅  Cadastrar Avaliação", self._register_assessment, width=240).pack(anchor="w", padx=16, pady=(10, 16))

    def _register_assessment(self):
        _set_msg(self._lbl_msg, "")
        try:
            weight = float(self._txt_weight.get().replace(",", "."))
        except ValueError:
            _set_msg(self._lbl_msg, "Peso inválido. Use um número como 0.40.", success=False)
            return
        try:
            msg = self._controller.register_assessment(
                self._txt_class.get(), self._txt_name.get(), weight
            )
            _set_msg(self._lbl_msg, msg, success=True)
            self._txt_class.delete(0, "end")
            self._txt_name.delete(0, "end")
            self._txt_weight.delete(0, "end")
        except Exception as ex:
            _set_msg(self._lbl_msg, str(ex), success=False)


# ── Visualização ──────────────────────────────────────────────────────────────

class VisualizationPanel(ctk.CTkFrame):
    def __init__(self, master, controller: AcademicSystemController):
        super().__init__(master, fg_color=C_BG)
        self.pack(fill="both", expand=True, padx=24, pady=24)
        self._controller = controller
        self._build()

    def _build(self):
        header = ctk.CTkFrame(self, fg_color=C_BG)
        header.pack(fill="x", pady=(0, 12))
        _label(header, "Turmas e Avaliações", font=FONT_TITLE, text_color=C_ACCENT).pack(side="left")
        _btn(header, "🔄 Atualizar", self._refresh, width=120).pack(side="right")

        self._txt = _textarea(self, height=450)
        self._txt.pack(fill="both", expand=True)
        self._refresh()

    def _refresh(self):
        self._txt.configure(state="normal")
        self._txt.delete("1.0", "end")
        try:
            content = self._controller.list_classes_and_assessments()
        except Exception as ex:
            content = f"Erro: {ex}"
        self._txt.insert("1.0", content)
        self._txt.configure(state="disabled")


# ── Relatórios ────────────────────────────────────────────────────────────────

class ReportPanel(ctk.CTkFrame):
    def __init__(self, master, controller: AcademicSystemController, user: User):
        super().__init__(master, fg_color=C_BG)
        self.pack(fill="both", expand=True, padx=24, pady=24)
        self._controller = controller
        self._user = user
        self._build()

    def _build(self):
        _label(self, "Relatórios", font=FONT_TITLE, text_color=C_ACCENT).pack(anchor="w", pady=(0, 12))

        btn_row = ctk.CTkFrame(self, fg_color=C_BG)
        btn_row.pack(fill="x", pady=(0, 16))

        _btn(btn_row, "📊 Resumo por Turma", self._report_summary, width=200).pack(side="left", padx=(0, 8))
        _btn(btn_row, "⚖️ Peso Avaliações", self._report_weight, width=180).pack(side="left", padx=(0, 8))

        if self._user.role == Role.ADMIN:
            _btn(btn_row, "💾 Config. Persistência", self._report_persistence, width=200, color="#5a4dbd").pack(side="left", padx=(0, 8))

        self._txt = _textarea(self, height=400)
        self._txt.pack(fill="both", expand=True)

    def _set_text(self, text: str):
        self._txt.configure(state="normal")
        self._txt.delete("1.0", "end")
        self._txt.insert("1.0", text)
        self._txt.configure(state="disabled")

    def _report_summary(self):
        try:
            self._set_text(self._controller.generate_class_assessment_summary_report())
        except Exception as ex:
            self._set_text(f"Erro: {ex}")

    def _report_weight(self):
        try:
            self._set_text(self._controller.generate_assessment_weight_report())
        except Exception as ex:
            self._set_text(f"Erro: {ex}")

    def _report_persistence(self):
        try:
            self._set_text(self._controller.generate_persistence_configuration_report())
        except Exception as ex:
            self._set_text(f"Erro: {ex}")


# ── Persistência ──────────────────────────────────────────────────────────────

class PersistencePanel(ctk.CTkFrame):
    def __init__(self, master, controller: AcademicSystemController):
        super().__init__(master, fg_color=C_BG)
        self.pack(fill="both", expand=True, padx=24, pady=24)
        self._controller = controller
        self._build()

    def _build(self):
        _label(self, "Configurar Persistência", font=FONT_TITLE, text_color=C_ACCENT).pack(anchor="w", pady=(0, 20))

        card = _card(self)
        card.pack(fill="x", ipadx=20, ipady=20)

        _label(card, "Selecione o tipo de persistência:", font=FONT_SUB).pack(anchor="w", padx=16, pady=(16, 12))

        self._var = ctk.StringVar(value=self._controller.get_current_persistence_type().name)

        for pt in PersistenceType:
            rb = ctk.CTkRadioButton(
                card, text=f"  {pt.description}",
                variable=self._var, value=pt.name,
                font=FONT_BODY, text_color=C_TEXT,
                fg_color=C_ACCENT, hover_color=C_ACCENT2,
            )
            rb.pack(anchor="w", padx=24, pady=6)

        self._lbl_msg = _msg_label(card)
        self._lbl_msg.pack(anchor="w", padx=16, pady=(8, 0))

        _btn(card, "✅  Confirmar", self._confirm, width=200).pack(anchor="w", padx=16, pady=(10, 16))

    def _confirm(self):
        try:
            pt = PersistenceType[self._var.get()]
            msg = self._controller.configure_persistence_type(pt)
            _set_msg(self._lbl_msg, msg, success=True)
        except Exception as ex:
            _set_msg(self._lbl_msg, str(ex), success=False)


# ── App principal ─────────────────────────────────────────────────────────────

class AcademicSystemApp(ctk.CTk):
    def __init__(self, controller: AcademicSystemController):
        super().__init__()
        self._controller = controller
        self.title("Sistema Acadêmico")
        self.geometry("1050x680")
        self.minsize(900, 580)
        self.configure(fg_color=C_BG)
        self._show_login()

    def _clear(self):
        for w in self.winfo_children():
            w.destroy()

    def _show_login(self):
        self._clear()
        LoginScreen(self, self._controller, self._on_login_success)

    def _on_login_success(self, user: User):
        self._clear()
        MainScreen(self, self._controller, user, self._show_login)
