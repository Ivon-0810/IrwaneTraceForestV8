# -*- coding: utf-8 -*-
"""
IrwaneTraceForest (ITF) - Lanceur bureau
Encapsule le serveur Flask local dans une fenêtre native (pywebview) afin de
produire une véritable application de bureau (.exe) avec PyInstaller.

Propriétaire exclusif : Gauthier MBILI (myvongauthier@gmail.com)
NE PAS DISTRIBUER CE FICHIER SOURCE. Seul l'exécutable compilé (.exe) doit
être livré aux sociétés clientes (SOFOCAM, ALPICAM, PALLISCO, SEFAC, etc.).
"""

import threading
import time
import socket

from database import init_db
from app import app


def port_libre(host="127.0.0.1", port=5000) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) != 0


def lancer_serveur_flask():
    init_db(reset=False)
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)


def main():
    thread_serveur = threading.Thread(target=lancer_serveur_flask, daemon=True)
    thread_serveur.start()

    # Laisse le temps au serveur Flask local de démarrer avant d'ouvrir la fenêtre
    for _ in range(50):
        if not port_libre():
            break
        time.sleep(0.1)

    try:
        import webview
        webview.create_window(
            "IrwaneTraceForest — ERP Traçabilité Forestière",
            "http://127.0.0.1:5000",
            width=1440,
            height=900,
            min_size=(1100, 700),
        )
        webview.start()
    except ImportError:
        # Repli si pywebview n'est pas installé : ouvre le navigateur par défaut.
        import webbrowser
        webbrowser.open("http://127.0.0.1:5000")
        print("pywebview n'est pas installé — ouverture dans le navigateur par défaut.")
        print("Fermez cette fenêtre de console pour arrêter le serveur ITF.")
        while True:
            time.sleep(3600)


if __name__ == "__main__":
    main()
