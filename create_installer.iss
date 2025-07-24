; Script de instalação para o Ragner
; Criado com Inno Setup

#define MyAppName "Ragner"
#define MyAppVersion "1.0"
#define MyAppPublisher "Your Name"
#define MyAppExeName "Ragner.exe"

[Setup]
AppId={{4B6674E4-5391-4D84-8791-85F8297D3816}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={localappdata}\{#MyAppName}
DisableProgramGroupPage=yes
UninstallDisplayIcon={app}\{#MyAppExeName}
Compression=lzma
SolidCompression=yes
OutputDir=installer
OutputBaseFilename=Ragner_Setup
WizardStyle=modern
PrivilegesRequired=lowest
AppMutex={#MyAppName}
CloseApplications=yes
UsePreviousAppDir=no 
CreateUninstallRegKey=yes
UpdateUninstallLogAppName=yes

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"
Name: "documentsfolder"; Description: "{cm:DocumentsFolder}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "dist\Ragner.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "remove_env_var.ps1"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\Ragner - Executar"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{autodesktop}\Ragner - Documentos"; Filename: "{localappdata}\{#MyAppName}\documentos"; Tasks: documentsfolder

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Dirs]
Name: "{localappdata}\{#MyAppName}\database"; Flags: uninsneveruninstall
Name: "{localappdata}\{#MyAppName}\documentos"; Flags: uninsneveruninstall
Name: "{localappdata}\{#MyAppName}\faiss_index"; Flags: uninsneveruninstall

[CustomMessages]
brazilianportuguese.DetectPrevious=Uma instalação anterior do Ragner foi detectada. O que você deseja fazer?
brazilianportuguese.UpdateProgram=Atualizar o programa
brazilianportuguese.UninstallProgram=Desinstalar o programa
brazilianportuguese.UninstallFailed=A desinstalação falhou com código: %1.
brazilianportuguese.RemoveData=Deseja remover todos os dados do aplicativo (banco de dados, documentos e índices)?
brazilianportuguese.UninstallOnly=O programa será desinstalado. Deseja continuar?
brazilianportuguese.UninstallComplete=Ragner foi desinstalado com sucesso!%n%nA variável de ambiente OPENAI_API_KEY também foi removida do sistema.
brazilianportuguese.ExitSetup=Fechar
brazilianportuguese.UpdateConfirm=O programa será atualizado, mantendo todos os seus dados. Deseja continuar?
brazilianportuguese.UninstallFinished=Desinstalação Concluída
brazilianportuguese.DocumentsFolder=Criar atalho para pasta de documentos

[Code]
// Função para suprimir o diálogo de cancelamento
procedure CancelButtonClick(CurPageID: Integer; var Cancel, Confirm: Boolean);
begin
  Cancel := True;
  Confirm := False;  // Não mostrar confirmação de cancelamento
end;

// Função para suprimir mensagem de cancelamento
function CancelWithoutPrompt(): Boolean;
begin
  Result := True;
end;

var
  PreviousInstalled: Boolean;
  PreviousUninstaller: String;
  TargetDir: String; // Variável para armazenar o diretório de destino
  ShouldMigrate: Boolean;
  BackupDir: String;
  OptionPage: TInputOptionWizardPage;
  UninstallCompletePage: TWizardPage;
  UninstallCompleteLabel: TNewStaticText;
  AbortInstallation: Boolean;

// Função para criar uma pasta de backup com carimbo de data/hora
function CreateBackupDir: String;
var
  TimeStamp: String;
begin
  TimeStamp := GetDateTimeString('yyyy-mm-dd_hh-nn-ss', '-', '-');
  Result := ExpandConstant('{localappdata}\Ragner_Backup_') + TimeStamp;
  ForceDirectories(Result);
end;

procedure InitializeWizard;
begin
  // Define o diretório de destino padrão
  TargetDir := ExpandConstant('{localappdata}\{#MyAppName}');
  BackupDir := '';
  ShouldMigrate := False;
  AbortInstallation := False;
  
  // Criar página de opções para instalação existente
  OptionPage := CreateInputOptionPage(wpWelcome,
    'Instalação existente', 'Foi detectada uma instalação existente',
    'O que você deseja fazer com a instalação existente?',
    True, False);
  OptionPage.Add('Atualizar o programa');
  OptionPage.Add('Desinstalar o programa');
  OptionPage.Values[0] := True; // Padrão: atualizar
  OptionPage.Values[1] := False; // Padrão: não desinstalar
  
  // Criar página de conclusão da desinstalação
  UninstallCompletePage := CreateCustomPage(wpWelcome, 
    ExpandConstant('{cm:UninstallFinished}'), 
    ExpandConstant('{cm:UninstallComplete}'));
  
  UninstallCompleteLabel := TNewStaticText.Create(UninstallCompletePage);
  UninstallCompleteLabel.Parent := UninstallCompletePage.Surface;
  UninstallCompleteLabel.Left := 0;
  UninstallCompleteLabel.Top := 0;
  UninstallCompleteLabel.Width := UninstallCompletePage.SurfaceWidth;
  UninstallCompleteLabel.Height := UninstallCompletePage.SurfaceHeight;
  UninstallCompleteLabel.Caption := ExpandConstant('{cm:UninstallComplete}');
  UninstallCompleteLabel.WordWrap := True;
end;

// Esta função determina se uma página deve ser pulada
function ShouldSkipPage(PageID: Integer): Boolean;
begin
  Result := False;
  
  // Pular a página de opções se não houver instalação prévia
  if (PageID = OptionPage.ID) and (not PreviousInstalled) then
    Result := True;
    
  // Pular a página de desinstalação concluída se não estivermos desinstalando apenas
  if (PageID = UninstallCompletePage.ID) and (not AbortInstallation) then
    Result := True;
    
  // Pular todas as páginas de instalação se estivermos apenas desinstalando
  if (AbortInstallation) and (PageID <> UninstallCompletePage.ID) and (PageID <> wpFinished) then
    Result := True;
end;

function InitializeSetup: Boolean;
var
  RegKey: String;
  RegValue: String;
  UninstallKey: String;
  RegKeys: TArrayOfString;
  I: Integer;
  OldDir: String;
  OldDir3: String;
begin
  // Verificar se existe uma instalação prévia
  PreviousInstalled := False;
  
  // Chave atual do Ragner
  UninstallKey := '{4B6674E4-5391-4D84-8791-85F8297D3816}_is1';
  RegKey := 'Software\Microsoft\Windows\CurrentVersion\Uninstall\' + UninstallKey;
  
  // Verificar em HKEY_CURRENT_USER
  if RegQueryStringValue(HKEY_CURRENT_USER, RegKey, 'UninstallString', RegValue) then
  begin
    PreviousInstalled := True;
    PreviousUninstaller := RegValue;
  end
  // Se não encontrar, verificar em HKEY_LOCAL_MACHINE
  else if IsAdmin() and RegQueryStringValue(HKEY_LOCAL_MACHINE, RegKey, 'UninstallString', RegValue) then
  begin
    PreviousInstalled := True;
    PreviousUninstaller := RegValue;
  end
  // Verificar também por outras possíveis instalações do Ragner (usando busca nas subchaves)
  else if RegKeyExists(HKEY_CURRENT_USER, 'Software\Microsoft\Windows\CurrentVersion\Uninstall') then
  begin
    if RegGetSubkeyNames(HKEY_CURRENT_USER, 'Software\Microsoft\Windows\CurrentVersion\Uninstall', RegKeys) then
    begin
      for I := 0 to GetArrayLength(RegKeys) - 1 do
      begin
        if Pos('Ragner', RegKeys[I]) > 0 then
        begin
          if RegQueryStringValue(HKEY_CURRENT_USER, 'Software\Microsoft\Windows\CurrentVersion\Uninstall\' + RegKeys[I], 'UninstallString', RegValue) then
          begin
            PreviousInstalled := True;
            PreviousUninstaller := RegValue;
            break;
          end;
        end;
      end;
    end;
  end;

  // Verificar também se as pastas existem, mesmo sem registro de instalação
  OldDir := ExpandConstant('{localappdata}\Ragner');
  OldDir3 := ExpandConstant('{localappdata}\Ragner3');
  
  if DirExists(OldDir) or DirExists(OldDir3) then
  begin
    PreviousInstalled := True;
  end;

  // Se não encontrou instalação anterior, não precisa mostrar opções
  // Não fazemos nada aqui, vamos controlar isso na função ShouldSkipPage
  
  Result := True;
end;

function NextButtonClick(CurPageID: Integer): Boolean;
var
  ResultCode: Integer;
  Params: String;
  UninstallStatus: Boolean;
  UninstallExe: String;
begin
  Result := True;
  
  // Se estamos na página de opções e tem instalação prévia
  if (CurPageID = OptionPage.ID) and PreviousInstalled then
  begin
    // Se escolheu desinstalar
    if OptionPage.Values[1] then
    begin
      // Confirmar desinstalação sem possibilidade de cancelamento
      if MsgBox(ExpandConstant('{cm:UninstallOnly}'), mbConfirmation, MB_YESNO) = IDYES then
      begin
        // Verificar se existe o desinstalador nativo unins000.exe
        UninstallExe := ExpandConstant('{localappdata}\{#MyAppName}\unins000.exe');
        
        UninstallStatus := True;
        
        // Primeiro tentar usar o desinstalador nativo (unins000.exe) 
        if FileExists(UninstallExe) then
        begin
          Exec(UninstallExe, '/SILENT', '', SW_SHOW, ewWaitUntilTerminated, ResultCode);
        end
        // Se não encontrar, usar o desinstalador registrado no sistema
        else if PreviousUninstaller <> '' then
        begin
          Exec(RemoveQuotes(PreviousUninstaller), '/SILENT', '', SW_SHOW, ewWaitUntilTerminated, ResultCode);
        end;

        // Garantir que os diretórios sejam removidos manualmente se necessário
        try
          if DirExists(ExpandConstant('{localappdata}\Ragner')) then
            DelTree(ExpandConstant('{localappdata}\Ragner'), True, True, True);
          if DirExists(ExpandConstant('{localappdata}\Ragner3')) then
            DelTree(ExpandConstant('{localappdata}\Ragner3'), True, True, True);
        except
          // Se houve erro na remoção de diretórios, apenas continue
        end;

        // Mostrar mensagem de confirmação
        MsgBox(ExpandConstant('{cm:UninstallComplete}'), mbInformation, MB_OK);
        
        // Encerrar o instalador após a desinstalação sem dar opção de cancelar
        WizardForm.Close();
        Result := False;
        Exit;
      end
      else
      begin
        // Se não quis desinstalar, prosseguir com atualização em vez de cancelar
        OptionPage.Values[0] := True;
        OptionPage.Values[1] := False;
        Result := True;
      end;
    end
    else if OptionPage.Values[0] then
    begin
      // Confirmar atualização - sempre prosseguir sem cancelar
      if MsgBox(ExpandConstant('{cm:UpdateConfirm}'), mbConfirmation, MB_YESNO) = IDNO then
      begin
        // Mesmo se cancelou a confirmação, prosseguir com a instalação padrão
        // em vez de abortar completamente
      end;
      
      // Configurar parâmetros para desinstalação mantendo dados
      Params := '/SILENT';
      
      // Executar o desinstalador se existir
      if PreviousUninstaller <> '' then
      begin
        Exec(RemoveQuotes(PreviousUninstaller), Params, '', SW_SHOW, ewWaitUntilTerminated, ResultCode);
      end;
      
      // Definir flag para migrar na instalação
      ShouldMigrate := True;
      Result := True;
    end;
  end
  // Na página de conclusão da desinstalação, apenas fechar o instalador
  else if (CurPageID = UninstallCompletePage.ID) or 
          ((AbortInstallation) and (CurPageID = wpFinished)) then
  begin
    // Sair do instalador ao pressionar Avançar na página de desinstalação concluída
    Result := False;
    WizardForm.Close;
  end;
end;

// Alterar o texto do botão Avançar na página de desinstalação concluída
procedure CurPageChanged(CurPageID: Integer);
begin
  if CurPageID = UninstallCompletePage.ID then
  begin
    WizardForm.NextButton.Caption := ExpandConstant('{cm:ExitSetup}');
    WizardForm.CancelButton.Visible := False;
  end;
end;

// Esta função é chamada após o diretório ser escolhido e também após a instalação estar completa
procedure CurStepChanged(CurStep: TSetupStep);
var
  OldDir: String;
  OldDir3: String;
begin
  if CurStep = ssInstall then
  begin
    // Agora podemos usar {app} com segurança pois o diretório já foi escolhido
    OldDir := ExpandConstant('{localappdata}\Ragner');
    OldDir3 := ExpandConstant('{localappdata}\Ragner3');
    
    // Se devemos migrar os dados de instalações anteriores
    if ShouldMigrate then
    begin
      // Migrar dados do Ragner (pasta original) se existir
      if DirExists(OldDir) and (CompareText(OldDir, ExpandConstant('{app}')) <> 0) then
      begin
        // Criar os diretórios necessários no destino
        ForceDirectories(ExpandConstant('{app}\database'));
        ForceDirectories(ExpandConstant('{app}\documentos'));
        ForceDirectories(ExpandConstant('{app}\faiss_index'));
        
        // Copiar os dados
        CopyFile(OldDir + '\database\*', ExpandConstant('{app}\database\*'), False);
        CopyFile(OldDir + '\documentos\*', ExpandConstant('{app}\documentos\*'), False); 
        CopyFile(OldDir + '\faiss_index\*', ExpandConstant('{app}\faiss_index\*'), False);
      end;
      
      // Migrar dados do Ragner3 (pasta incorreta) se existir
      if DirExists(OldDir3) then
      begin
        // Criar os diretórios necessários no destino
        ForceDirectories(ExpandConstant('{app}\database'));
        ForceDirectories(ExpandConstant('{app}\documentos'));
        ForceDirectories(ExpandConstant('{app}\faiss_index'));
        
        // Copiar os dados
        CopyFile(OldDir3 + '\database\*', ExpandConstant('{app}\database\*'), False);
        CopyFile(OldDir3 + '\documentos\*', ExpandConstant('{app}\documentos\*'), False); 
        CopyFile(OldDir3 + '\faiss_index\*', ExpandConstant('{app}\faiss_index\*'), False);
      end;
    end;
  end
  else if CurStep = ssPostInstall then
  begin
    // Se escolhemos manter os dados mas migrar, agora podemos remover as pastas antigas
    if ShouldMigrate then
    begin
      OldDir := ExpandConstant('{localappdata}\Ragner');
      OldDir3 := ExpandConstant('{localappdata}\Ragner3');
      
      if DirExists(OldDir) and (CompareText(OldDir, ExpandConstant('{app}')) <> 0) then
      begin
        DelTree(OldDir, True, True, True);
      end;
      
      if DirExists(OldDir3) then
      begin
        DelTree(OldDir3, True, True, True);
      end;
    end;
  end;
end;

// Esta função é chamada durante o processo de desinstalação
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  MsgResult: Integer;
  VariavelRemovida: Boolean;
begin
  if CurUninstallStep = usUninstall then
  begin
    MsgResult := IDNO;
    
    if ExpandConstant('{param:REMOVEDATA|0}') = '1' then
      MsgResult := IDYES
    else
      MsgResult := MsgBox(ExpandConstant('{cm:RemoveData}'), mbConfirmation, MB_YESNO);
    
    if MsgResult = IDYES then
    begin
      // Remover os dados
      DelTree(ExpandConstant('{localappdata}\{#MyAppName}\database'), True, True, True);
      DelTree(ExpandConstant('{localappdata}\{#MyAppName}\documentos'), True, True, True);
      DelTree(ExpandConstant('{localappdata}\{#MyAppName}\faiss_index'), True, True, True);
      DelTree(ExpandConstant('{localappdata}\{#MyAppName}'), False, False, False);
      
      // Garantir que as pastas antigas também sejam removidas
      DelTree(ExpandConstant('{localappdata}\Ragner'), True, True, True);
      DelTree(ExpandConstant('{localappdata}\Ragner3'), True, True, True);
    end;
    
    // Remover a variável de ambiente OPENAI_API_KEY (sempre remove, independente da escolha dos dados)
    VariavelRemovida := False;
    
    // Método 1: Executar script PowerShell (mais confiável e robusto)
    if FileExists(ExpandConstant('{app}\remove_env_var.ps1')) then
    begin
      if Exec('powershell.exe', '-ExecutionPolicy Bypass -File "' + ExpandConstant('{app}\remove_env_var.ps1') + '"', '', SW_HIDE, ewWaitUntilTerminated, MsgResult) then
      begin
        if MsgResult = 0 then VariavelRemovida := True;
      end;
    end;
    
    // Método 2: Usar REG DELETE diretamente (backup)
    if not VariavelRemovida then
    begin
      if Exec('reg.exe', 'query "HKEY_CURRENT_USER\Environment" /v OPENAI_API_KEY', '', SW_HIDE, ewWaitUntilTerminated, MsgResult) then
      begin
        if MsgResult = 0 then // Variável existe
        begin
          Exec('reg.exe', 'delete "HKEY_CURRENT_USER\Environment" /v OPENAI_API_KEY /f', '', SW_HIDE, ewWaitUntilTerminated, MsgResult);
          if MsgResult = 0 then VariavelRemovida := True;
        end;
      end;
    end;
    
    // Método 3: Usar as funções do Inno Setup como último recurso
    if not VariavelRemovida and RegValueExists(HKEY_CURRENT_USER, 'Environment', 'OPENAI_API_KEY') then
    begin
      if RegDeleteValue(HKEY_CURRENT_USER, 'Environment', 'OPENAI_API_KEY') then
        VariavelRemovida := True;
    end;
    
    // Se for administrador, tentar remover também da variável de sistema
    if IsAdmin() then
    begin
      if Exec('reg.exe', 'query "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v OPENAI_API_KEY', '', SW_HIDE, ewWaitUntilTerminated, MsgResult) then
      begin
        if MsgResult = 0 then // Variável existe no sistema
        begin
          Exec('reg.exe', 'delete "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v OPENAI_API_KEY /f', '', SW_HIDE, ewWaitUntilTerminated, MsgResult);
        end;
      end;
      
      // Backup usando funções do Inno Setup
      if RegValueExists(HKEY_LOCAL_MACHINE, 'SYSTEM\CurrentControlSet\Control\Session Manager\Environment', 'OPENAI_API_KEY') then
      begin
        RegDeleteValue(HKEY_LOCAL_MACHINE, 'SYSTEM\CurrentControlSet\Control\Session Manager\Environment', 'OPENAI_API_KEY');
      end;
    end;
  end;
end;

// Função para inicializar o desinstalador
function InitializeUninstall(): Boolean;
begin
  // Sempre retornar verdadeiro para continuar com a desinstalação
  Result := True;
end;

// Função para lidar com cliques nos botões do desinstalador
function UninstallButtonClick(CurUninstallStep: TUninstallStep; ButtonID: Integer): Boolean;
begin
  // Sempre permitir que o botão funcione, independente da Passo
  Result := True;
end;