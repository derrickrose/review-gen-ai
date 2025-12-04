# Récupération du token OPENAI_API_KEY

1.  **Créer un compte OpenAI** :

    -   Inscris-toi ou connecte-toi sur https://platform.openai.com/.

2.  **Obtenir la clé API OpenAI** :

    -   Va dans Dashboard → API Keys.
    -   Clique sur "Create new secret key".
    -   Copie la clé affichée (elle commence par sk-...).

3.  **Définir la clé API comme variable d'environnement** :

    **Sur Windows (PowerShell)** :

    ``` bash
    $env:OPENAI_API_KEY="ta_cle_api_ici"
    ```

    **Sur macOS / Linux** :

    ``` bash
    export OPENAI_API_KEY="ta_cle_api_ici"
    source ~/.bashrc   # ou source ~/.zshrc
    ```

4.  **Vérifier la variable d'environnement** :

    -   **Windows :**

    ``` bash
    echo $env:OPENAI_API_KEY
    ```

    -   **macOS / Linux :**

    ``` bash
    echo $OPENAI_API_KEY
    ```

### Conclusion :

Avec cette configuration, ton application peut accéder à l'API OpenAI en
toute sécurité.
