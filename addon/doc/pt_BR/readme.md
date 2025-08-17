# Gerenciador de Pomodoros para NVDA

## Descrição

O **Gerenciador de Pomodoros** é um complemento para o leitor de tela NVDA que implementa a técnica Pomodoro, ajudando os usuários a gerenciar seus tempos de trabalho e descanso de forma eficaz.  
A técnica Pomodoro envolve dividir o tempo de trabalho em intervalos (tradicionalmente de 25 minutos), separados por pequenas pausas.  
Este complemento é ideal para usuários que desejam melhorar a produtividade e gerenciar melhor o tempo enquanto utilizam o NVDA.

## Como Funciona

Uma vez ativado, o complemento permite iniciar, pausar, retomar ou parar o cronômetro Pomodoro usando atalhos de teclado específicos.  
Além disso, fornece feedback auditivo e verbal no início e no final de cada sessão de trabalho ou descanso.  
O complemento gerencia automaticamente os ciclos de trabalho e descanso, incluindo pausas longas após cada quatro ciclos de trabalho concluídos.

### Atalhos de Teclado
Os atalhos de teclado devem ser atribuídos a partir da opção **Gestos de Entrada** no menu **Preferências** do NVDA.  
As opções podem ser encontradas na categoria **Gerenciador de Pomodoros**.

## Registro de Alterações
### 1.16
- Adicionada compatibilidade com a versão NVDA 2025.1.

### 1.15
- Tradução russa atualizada. [PR #3](https://github.com/jpavonabian/gestor-de-Pomodoros/pull/3)

### 1.14
- Adicionada tradução para o russo. Obrigado, [Валентин Куприянов: Русский язык](https://nvda.ru/)

### 1.11
- Atualizado para a versão de testes mais recente do NVDA.

### 1.10
- Corrigido um erro em que o tempo continuava avançando mesmo quando um Pomodoro estava pausado.

### 1.9
- Alterado o nome interno do complemento para evitar problemas com a loja oficial.

### 1.8
- Corrigido um erro de Braille e mensagens.  
- Corrigido um problema de gerenciamento de tempo.  
- Grande parte do código interno foi refatorada.

### 1.7
- Corrigido um erro no canal de distribuição.  
- Corrigido um bug ao tentar parar um Pomodoro que ainda não havia sido iniciado.

### 1.6
- Alterada a duração e frequência dos tons.  
- As mensagens do complemento agora têm alta prioridade para garantir que não sejam perdidas durante outras atividades.  
- Os tons não são mais reproduzidos apenas no canal direito; isso era um erro.

### 1.5
- Os atalhos de teclado foram removidos. Agora devem ser atribuídos pelo usuário.

### 1.4
- Atalhos de teclado atualizados para maior intuitividade.  
- Pequenos ajustes no código interno.  
- Os atalhos agora aparecem corretamente nas categorias de gestos.

### 1.3
- Gestos de entrada agora podem ser reatribuídos na categoria **Gerenciador de Pomodoros**. [PR #1](https://github.com/jpavonabian/Gestor-de-Pomodoros/pull/1)

### 1.2
- Corrigido o tratamento interno do complemento pelo NVDA.

### 1.1
- O complemento não funciona em telas seguras.  
- Processo de lançamento automatizado usando GitHub Actions.

### 1.0
- Lançamento inicial do complemento.  
- Funcionalidade básica do Pomodoro implementada, incluindo iniciar, pausar, retomar e parar o cronômetro.  
- Anúncios auditivos e verbais para o início e o fim das sessões de trabalho e descanso.

## Agradecimentos Especiais
- A **Sukil Etxenike** <sukiletxe@yahoo.es> por me colocar no caminho certo quando eu não tinha experiência em desenvolver complementos e não sabia por onde começar.  
- A **Ángel Alcántar** <rayoalcantar@gmail.com> pela revisão do código.  
- A **Noelia Ruiz Martínez** <nrm1977@gmail.com> pelo feedback sobre o código e por aguentar tantas perguntas de iniciante.
