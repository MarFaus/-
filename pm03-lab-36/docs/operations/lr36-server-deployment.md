# ЛР №36. Развертывание Cloud Application на сервере (без Docker)

Эксплуатационная заметка. Секреты и пароли в документ не включаются.

## Паспорт среды

| Параметр | Значение |
|---|---|
| ОС | Ubuntu Server 24.04.5 LTS (учебный стенд) |
| Менеджер служб | systemd |
| Пользователь приложения | `cloudapp` (nologin) |
| Код приложения | `/opt/cloud-application/app` (Git, ветка main, commit `a4d289f`) |
| Python-окружение | `/opt/cloud-application/venv` |
| Конфигурация | `/etc/cloud-application/cloud-application.env` (root:cloudapp, 0640) |
| Секреты | `/etc/cloud-application/secrets` (root:cloudapp, 0750), ссылка `app/secrets` |
| Служба | `cloud-application.service` |
| Адрес и порт | `127.0.0.1:8000` |
| Журнал | systemd journal |

## Последовательность deployment

```bash
sudo apt update && sudo apt install -y git python3 python3-venv python3-pip curl
sudo useradd --system --user-group --home-dir /opt/cloud-application --shell /usr/sbin/nologin cloudapp
sudo install -d -o cloudapp -g cloudapp -m 0755 /opt/cloud-application
sudo install -d -o root -g cloudapp -m 0750 /etc/cloud-application
sudo -u cloudapp git clone https://github.com/MarFaus/Cloud-Application.git /opt/cloud-application/app
sudo -u cloudapp git -C /opt/cloud-application/app rev-parse --short HEAD
sudo -u cloudapp python3 -m venv /opt/cloud-application/venv
sudo -u cloudapp /opt/cloud-application/venv/bin/python -m pip install -r /opt/cloud-application/app/requirements.txt
sudo -u cloudapp /opt/cloud-application/venv/bin/python -m pip check
# env-файл, каталог secrets, ссылка app/secrets и unit-файл: см. results/ и отчёт
sudo systemd-analyze verify /etc/systemd/system/cloud-application.service
sudo systemctl daemon-reload
sudo systemctl enable --now cloud-application.service
```

## Smoke-test

```bash
systemctl is-enabled cloud-application.service     # enabled
systemctl is-active cloud-application.service      # active
sudo ss -ltnp | grep ':8000'                       # 127.0.0.1:8000
curl -i http://127.0.0.1:8000/status               # HTTP 200
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8000/docs   # 200
```

## Rollback конфигурации

```bash
sudo cp /etc/cloud-application/cloud-application.env /etc/cloud-application/cloud-application.env.bak
# ... изменение и сбой ...
sudo journalctl -u cloud-application.service -n 50 --no-pager   # причина отказа
sudo systemctl stop cloud-application.service
sudo cp /etc/cloud-application/cloud-application.env.bak /etc/cloud-application/cloud-application.env
sudo systemctl start cloud-application.service
curl -i http://127.0.0.1:8000/status                            # повторный smoke-test
sudo rm /etc/cloud-application/cloud-application.env.bak
```
