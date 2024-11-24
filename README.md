
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

Ouvrez un explorateur de fichiers et naviguez jusqu'au répertoire ou vous avez mis le code, rentrez dans le répertoire "JV-lyc-e-altitude-main" puis "Projet_jeu_vidéo" (vous devriez voir un fichier appelé "Main.py" ou "Main") et copiez le chemin. Ouvrez un terminal (ou powershell sous Windows) et écrivez "cd chemin/que/vous/avez/copié". ex:  
cd C:\Users\ellio\Downloads\JV-lyc-e-altitude-main\JV-lyc-e-altitude-main\Projet_jeu_vidéo

Ensuite, pour rentrer et sortir du répertoire "maps" (la ou se trouve l'éditeur de niveau) utilisez la commande "cd". "cd" va vous avancer dans le répertoire que vous lui donnez. ex: "cd maps" pour rentrer dans le répertoire "maps". Vous pouvez aussi lui donnez ".." pour remonter d'un répertoire. ex: "cd .." pour sortir du répertoire "maps".  

Verifiez que vous êtes dans le bon répertoire en utilisant la commande "ls". Cette commande va lister tous les fichiers et répertoires dans votre répertoire courrant. Si vous voyez un fichier appelé "Main.py" vous êtes au bon endroit!  

Lancez le jeu en lancant la commande "python Main.py". Si vous voyez un petit bonhomme que vous pouvez déplacer avec les fleches, félicitations! Vous avez réussi!

## Pour lancer l'éditeur de map:  

Rentrez dans le répertoire maps en utilisant la commande "cd maps".  

Vérifiez que vous etes au bon endroit avec la commande "ls" si vous voyez un fichier nomé "map_editor.py", alors c'est bon!  

Lancez l'éditeur avec la commande "python map_editor.py"

## Pour utiliser l'éditeur de map:  

### Les bases:

Une fois que vous avez lancé l'éditeur, vous etes prets a éditer la map!  

Vous pouvez lire les differentes commandes dans le menu aide, que vous pouvez montrer/cahcher avec "h". Toutes les commandes seront éxpliquées plus loin, l'aide sert plutot de "pense-bete".  

Déplacez vous dans la map en clickant et deplacant la souris.  

Zoomez/Dézoomez avec la molette de la souris.  

La barre de gauche est un liste de toutes les tuiles que vous avez a votre disposition pour éditer la map.  

Descendez/montez dans la barre de gauche en mettant la souris au dessus et en utilisant la molette de la souris.  

Choisisez une tuile dans la barre de gauche en cliquant dessus.  

Choisisez la couche sur laquelle vous voulez la placer en utilisant les fleches haut/bas pour monter/descendre d'une couche. Votre couche courante est écrite en haut a droite de la fenetre. La couche 0 est la plus basse (celle qui va etre affichée en dessous du reste).  

Placez cette tuile sur la map avec un click droit la ou vous voulez la placer.  

Appuyez sur "e" ou selectionnez la tuile grise dans la barre de gauche pour effacer des tuiles, toujours avec le click droit.  

Sauvegardez la map avec q, puis quitter avec esc.  

Si vous oubliez de sauvegarder la map avant de quitter, la fenetre va se fermer mais le terminal va vous demander si vous voulez le faire maintenant. Tapez "oui" si vous voulez la sauvegarder ou "non" si non, puis appuyez sur "entrer".  

Ouvrez le fichier "map.png", vous devriez voir la map dans son entiereté avec la nouvelle tuile que vous venez de placer.  

Vous pouvez aussi lancer le jeu et voir la map en action!  

### Commandes avancées:  

Pour défaire le dernier changement que vous avez fait, utilisez ctrl+z.  

Pour changer un groupe de tuiles en meme temps, restez appuyé sur maj gauche et déplacez la souris. Le rectangle gris represente les tuiles que vous allez modifier.  
Placer une tuile (click droit) alors que vous avez un rectangle selectioné va remplir votre selection avec cette tuile.  
Appuyer sur "c" alors que vous avez un rectangle selectioné va copier ce groupe de tuiles, que vous pouvez ensuite coller ou vous voulez avec "v".  

Pour dupliquer la tuile que vous survolez avec la souris, faisez un click milieu, ceci va vous permettre de placer la meme tuile autre part.

Pour reseter le zoom (le remettre a 1), appuyez sur "z".  

Pour rentrer/sortir du mode verbose, appuyez sur espace.  
Le mode verbose permet de voir le nom de chaque tuile, ainsi que tout ses attributs speciaux.  

Pour rajouter un attribut special a une tuile, utilisez ctrl+click gauche (quand vous survolez la tuile que vous voulez modifier) puis rentrez "nom_de_l_attribut:valeur", (n'utilisez pas de "," ni de ":" (sauf celui entre la valeur et le nom de l'attribut)) (ex: "collision:0"), vous pouvez rajouter plusieurs attributs d'un coup en séparant chaque paire d'attribut/valeur avec une virgule, puis appuyez sur entrer. Pour modifier les attributs speciaux de tuiles, il est recommandé d'activer le mode verbose.  

Pour enlever TOUT les attributs spéciaux d'une tuile, utilisez ctrl+click droit (quand vous survolez la tuile que vous voulez modifier).  

### Modifier attributs.py pour rajouter des tuiles et modifier les parametres de la map:  

Pour rajouter un type de tuile se trouvant dans un fichier image unique a cette tuile:  
Copiez le fichier image dans le répertoire collisions dans le répertoire maps.  
Suivez les instructions dans attributs.py.  

Pour rajouter plusieurs types de tuiles se trouvant dans une tilemap:
Copiez le fichier image dans le répertoire tilemaps dans le répertoire maps.  
Suivez les instructions dans attributs.py.  

Pour modifier les parametres de la map:
Trouvez le parametre que vous voulez modifier grace au commentaires (lignes commencant avec "#"). Ces commentaires expliquent ce que chaque paremetre fait.  
Modifiez la valeur qui se trouve apres le "=". Si cette valeur se trouve entre guillemets, alors LAISSEZ LES GUILLEMETS, et rentrez ce que vous voulez entre. Sinon, cette valeur doit etre un nombre entier (ex: 12).

## Pour avoir de l'aide:  

Demandez sur le discord! :)