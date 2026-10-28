# TaskFlow Dashboard

Frontend React + TypeScript para a API FastAPI deste repositório. A interface consome diretamente `/projetos` e `/tarefas`, sem autenticação ou armazenamento adicional.

## Executar localmente

1. Inicie a API seguindo as instruções do README principal do repositório; ela deve responder em `http://localhost:8000`.
2. Instale pnpm 11.25.0 (ou use Corepack) e instale as dependências:

   ```sh
   pnpm install
   cp .env.example .env.local
   pnpm dev
   ```

3. Acesse o endereço exibido pelo Vite. Por padrão, o frontend chama `/api` e o Vite encaminha essas chamadas à API em `http://localhost:8000`, removendo o prefixo `/api`; assim, o fluxo local não depende de CORS.

Altere `TASKFLOW_API_TARGET` em `.env.local` se a API estiver em outro endereço. `VITE_API_BASE_URL` pode apontar diretamente para outra URL-base da API; nesse caso, o servidor da API deve permitir a origem do frontend via CORS. O valor configurado é público no bundle e não deve conter segredos.

## Build

```sh
pnpm build
```

A saída estática fica em `dist/`. A API existente continua sendo executada separadamente.
