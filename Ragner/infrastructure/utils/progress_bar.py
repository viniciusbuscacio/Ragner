#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Utilitário para exibir barras de progresso no terminal.
"""

import sys
import time
from typing import Optional

class ProgressBar:
    """
    Classe para exibir barras de progresso no terminal de forma educativa.
    """
    
    def __init__(self, total: int, prefixo: str = "Progresso", largura: int = 40):
        """
        Inicializa a barra de progresso.
        
        Args:
            total: Número total de itens a processar
            prefixo: Texto a exibir antes da barra
            largura: Largura da barra em caracteres
        """
        self.total = total
        self.prefixo = prefixo
        self.largura = largura
        self.atual = 0
        self.inicio = time.time()
    
    def atualizar(self, atual: Optional[int] = None, sufixo: str = ""):
        """
        Atualiza a barra de progresso.
        
        Args:
            atual: Progresso atual (se None, incrementa em 1)
            sufixo: Texto adicional a exibir no final
        """
        if atual is None:
            self.atual += 1
        else:
            self.atual = atual
        
        # Calcular porcentagem
        porcentagem = int((self.atual / self.total) * 100) if self.total > 0 else 0
        
        # Criar a barra visual
        preenchido = int((self.atual / self.total) * self.largura) if self.total > 0 else 0
        barra = '█' * preenchido + '░' * (self.largura - preenchido)
        
        # Calcular tempo estimado
        tempo_decorrido = time.time() - self.inicio
        if self.atual > 0:
            tempo_por_item = tempo_decorrido / self.atual
            tempo_restante = tempo_por_item * (self.total - self.atual)
            eta = f" ETA: {int(tempo_restante)}s" if tempo_restante > 1 else ""
        else:
            eta = ""
        
        # Exibir a barra (com espaçamento para limpar linha anterior)
        linha = f"\r{self.prefixo}: [{barra}] {porcentagem}% ({self.atual}/{self.total}){eta}"
        if sufixo:
            linha += f" - {sufixo}"
        
        # Limpar o resto da linha
        print(linha, end='', flush=True)
        
        # Nova linha quando completo
        if self.atual >= self.total:
            print()
    
    def finalizar(self, mensagem: str = "Concluído!"):
        """
        Finaliza a barra de progresso com uma mensagem.
        
        Args:
            mensagem: Mensagem final a exibir
        """
        if self.atual < self.total:
            self.atual = self.total
            self.atualizar()
        
        tempo_total = time.time() - self.inicio
        print(f"✓ {mensagem} (Tempo total: {tempo_total:.1f}s)")

def mostrar_progresso_simples(atual: int, total: int, prefixo: str = "Progresso", largura: int = 30):
    """
    Função utilitária para mostrar progresso de forma simples.
    
    Args:
        atual: Progresso atual
        total: Total de itens
        prefixo: Texto antes da barra
        largura: Largura da barra
    """
    porcentagem = int((atual / total) * 100) if total > 0 else 0
    preenchido = int((atual / total) * largura) if total > 0 else 0
    barra = '█' * preenchido + '░' * (largura - preenchido)
    
    print(f"\r{prefixo}: [{barra}] {porcentagem}% ({atual}/{total})", end='', flush=True)
    
    if atual >= total:
        print()  # Nova linha quando completo
