@echo off
echo ========================================
echo    DEPLOIEMENT PONGECHEC BACKEND
echo ========================================
echo.

REM Configuration des chemins
REM ATTENTION: Modifiez ce chemin selon votre installation WildFly
set WILDFLY_HOME=D:\wildfly-37.0.1.Final\wildfly-37.0.1.Final
set WILDFLY_DEPLOYMENTS=%WILDFLY_HOME%\standalone\deployments
set PROJECT_ROOT=%~dp0
set BACKEND_MODULE=%PROJECT_ROOT%backend

echo Configuration:
echo - WildFly Home: %WILDFLY_HOME%
echo - WildFly Deployments: %WILDFLY_DEPLOYMENTS%
echo - Backend: %BACKEND_MODULE%
echo.

REM Vérifier que WildFly existe
if not exist "%WILDFLY_HOME%" (
    echo ERREUR: WildFly introuvable: %WILDFLY_HOME%
    echo.
    echo Modifiez la variable WILDFLY_HOME dans ce script pour pointer vers votre installation WildFly.
    echo Exemple: set WILDFLY_HOME=G:\ITU\S5\PROG\wildfly\wildfly-27.0.0.Final
    pause
    exit /b 1
)

if not exist "%WILDFLY_DEPLOYMENTS%" (
    echo ERREUR: Répertoire de déploiement introuvable: %WILDFLY_DEPLOYMENTS%
    pause
    exit /b 1
)

REM Vérifier que le backend existe
if not exist "%BACKEND_MODULE%" (
    echo ERREUR: Module backend introuvable: %BACKEND_MODULE%
    pause
    exit /b 1
)

echo ========================================
echo 1. COMPILATION DU BACKEND
echo ========================================
cd /d "%BACKEND_MODULE%"
echo Compilation du projet Maven...
call mvn clean package
if %ERRORLEVEL% neq 0 (
    echo ERREUR: Échec de la compilation du backend
    pause
    exit /b 1
)
echo ✓ Backend compilé avec succès
echo.

echo ========================================
echo 2. DEPLOIEMENT SUR WILDFLY
echo ========================================

REM Supprimer l'ancien déploiement
echo Nettoyage des anciens déploiements...
if exist "%WILDFLY_DEPLOYMENTS%\pongechec.war" (
    del "%WILDFLY_DEPLOYMENTS%\pongechec.war"
    echo ✓ Ancien WAR supprimé
)
if exist "%WILDFLY_DEPLOYMENTS%\pongechec.war.deployed" (
    del "%WILDFLY_DEPLOYMENTS%\pongechec.war.deployed"
)
if exist "%WILDFLY_DEPLOYMENTS%\pongechec.war.failed" (
    del "%WILDFLY_DEPLOYMENTS%\pongechec.war.failed"
)

REM Déployer le nouveau WAR
echo Déploiement du module Backend...
if exist "%BACKEND_MODULE%\target\pongechec.war" (
    copy "%BACKEND_MODULE%\target\pongechec.war" "%WILDFLY_DEPLOYMENTS%\"
    echo ✓ Backend déployé: pongechec.war
) else (
    echo ERREUR: Fichier WAR introuvable: %BACKEND_MODULE%\target\pongechec.war
    pause
    exit /b 1
)

echo.
echo Attente du déploiement (15 secondes)...
timeout /t 15 /nobreak >nul

REM Vérifier le statut du déploiement
if exist "%WILDFLY_DEPLOYMENTS%\pongechec.war.deployed" (
    echo ✓ Application déployée avec succès
) else if exist "%WILDFLY_DEPLOYMENTS%\pongechec.war.failed" (
    echo ✗ ERREUR: Le déploiement a échoué
    echo Consultez les logs WildFly: %WILDFLY_HOME%\standalone\log\server.log
    pause
    exit /b 1
) else (
    echo ⚠ Statut de déploiement inconnu, vérifiez les logs
)

echo.
echo ========================================
echo 3. VERIFICATION DE L'API
echo ========================================
echo Test de l'API REST...
curl -s http://localhost:8080/pongechec/api/configurations >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo ✓ API REST accessible
) else (
    echo ⚠ API REST non accessible (WildFly peut ne pas être démarré)
    echo   Démarrez WildFly avec: %WILDFLY_HOME%\bin\standalone.bat
)

echo.
echo ========================================
echo ✓ DEPLOIEMENT TERMINE
echo ========================================
echo.
echo Application déployée:
echo - pongechec.war
echo.
echo URLs importantes:
echo - API REST: http://localhost:8080/pongechec/api/configurations
echo - Console WildFly: http://localhost:9990
echo.
echo PROCHAINES ETAPES:
echo 1. Si WildFly n'est pas démarré, lancez: %WILDFLY_HOME%\bin\standalone.bat
echo 2. Vérifiez que PostgreSQL est démarré avec la base 'pongechec_db'
echo 3. Testez l'API avec: curl http://localhost:8080/pongechec/api/configurations
echo 4. Testez le jeu Python avec: python test_backend.py
echo.
echo LOGS WILDFLY:
echo - Serveur: %WILDFLY_HOME%\standalone\log\server.log
echo - Déploiement: %WILDFLY_HOME%\standalone\log\server.log
echo.
pause

REM Retourner au répertoire initial
cd /d "%PROJECT_ROOT%"
