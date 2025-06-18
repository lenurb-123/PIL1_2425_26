function verifierMotDePasse() {
            const motdepasse = document.getElementById("motdepasse").value;
            const confirmpass = document.getElementById("confirmpass").value;
            const erreur = document.getElementById("erreur");

            if (motdepasse !== confirmpass) {
                erreur.style.display = "block";
                return false; // Empêche l'envoi du formulaire
            } else {
                erreur.style.display = "none";
                return true;
            }
        }