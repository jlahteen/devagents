@echo off
docker run -it -v C:\_temp\devagents:/devagents-ws --env-file ../.env-linux devagents
