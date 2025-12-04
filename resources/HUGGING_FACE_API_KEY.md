# Récupération token HUGGING_FACE_API_KEY

1. **Créer un compte Hugging Face** :
    - Inscris-toi sur [Hugging Face](https://huggingface.co/join).

2. **Obtenir la clé API** :
    - Connecte-toi à ton compte sur [Hugging Face Tokens](https://huggingface.co/settings/tokens).
    - Crée un nouveau **token** API ou copie un token existant.

3. **Définir la clé API comme variable d'environnement** :

   #### Sur Windows :
    - Ouvre **PowerShell** et exécute la commande suivante pour définir la variable :
      ```bash
      $env:HUGGING_FACE_API_KEY="ton_api_key_ici"
      ```
    - Pour la rendre permanente, ajoute-la dans les **variables système**.

   #### Sur macOS / Linux :
    - Ouvre ton terminal et ajoute cette ligne dans ton fichier `.bashrc` ou `.zshrc` :
      ```bash
      export HUGGING_FACE_API_KEY="ton_api_key_ici"
      ```
    - Recharge le fichier avec la commande :
      ```bash
      source ~/.bashrc   # ou source ~/.zshrc
      ```

4. **Vérifier la variable d'environnement** :
    - Pour vérifier que la clé est bien définie, exécute :
        - **Windows (PowerShell)** :
          ```bash
          echo $env:HUGGING_FACE_API_KEY
          ```
        - **macOS / Linux** :
          ```bash
          echo $HUGGING_FACE_API_KEY
          ```
