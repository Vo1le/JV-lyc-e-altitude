
# Jeux Vidéo du Lycée  

## Pour installer python et pygame:

Verifiez si vous avez déjà Python d'installé en lancant la commande "python --version" dans un terminal (ou powershell sous Windows). Ceci vous affichera la version de Python qui est installé sur votre ordinateur. Si le premier chiffre du retour et un "2" (ex: Python 2.7.3) alors vous devez télécharger un eversion plus récente: Python 3. Si vous recevez une erreur, c'est que python n'est pas installé sur votre ordinateur. Dans ces deux cas, procédez à la prochaine étape. Si le retour commence par "Python 3" alors vous avez la bonne version installé et vous pouvez passer directement a l'étape pour installer pygame  

Allez sur le site officiel : https://www.python.org/downloads/  

Choisissez la version adaptée à votre système d'exploitation (Windows, macOS, Linux).  

Téléchargez le fichier d'installation et exécutez-le.  

**IMPORTANT** Sur Windows, cochez la case "Ajouter Python à PATH" pour faciliter l'utilisation en ligne de commande; sur macOS et Linux, Python est généralement déjà dans le PATH.  

Cliquez sur "Install Now" (Windows) ou suivez les instructions à l'écran (macOS, Linux).  

Verifiez que vous avez bien installé Python en lancant la commande "python --version" dans un terminal (ou powershell sous Windows). Le retour devrait ressembler a "Python 3.12.3".

Pour installer pygame, lancez la commande "python -m pip install -U pygame --user"  

Verifiez que vous avez bien installez pygame, lancez la commande "python -m pygame.examples.aliens". Ceci devrait lancer un petit jeu "exemple" que vous pouvez quitter en clickant la croix en haut a droite.

## Pour installer le jeu:  

Cliquez sur le boutton "Code" vert, puis sur le boutton "Download ZIP".  

Dezipez le ZIP que vous venez d'installer dans un endroit ou vous pouvez le retrouver facilement.  

Ouvrez un explorateur de fichiers et naviguez jusqu'au répertoire ou vous avez mis le code, rentrez dans le répertoire "Projet jeu vidéo" et copiez le chemin. Ouvrez un terminal (ou powershell sous Windows) et écrivez "cd chemin/que/vous/avez/copié". ex:  
cd C:\Users\ellio\Documents\coding\Python\JV_Lycee\JV-lyc-e-altitude\Projet jeu vidéo>  

Ensuite, pour rentrer et sortir du répertoire "maps" (la ou se trouve l'éditeur de niveau) utilisez la commande "cd". "cd" va vous avancer dans le répertoire que vous lui donnez. ex: "cd maps" pour rentrer dans le répertoire "maps". Vous pouvez aussi lui donnez ".." pour remonter d'un répertoire. ex: "cd .." pour sortir du répertoire "maps".  

Verifiez que vous êtes dans le bon répertoire en utilisant la commande "ls". Cette commande va lister tous les fichiers et répertoires dans votre répertoire courrant. Si vous voyez un fichier appelé "Main.py" vous êtes au bon endroit!  

Lancez le jeu en lancant la commande "python .\Main.py". Si vous voyez un petit bonhomme que vous pouvez déplacer avec les fleches, félicitations! Vous avez réussi!