<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">
    <title>gpuview</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous"/>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" rel="stylesheet"/>
    <link href="https://cdn.datatables.net/2.0.3/css/dataTables.bootstrap5.min.css" rel="stylesheet"/>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🚀</text></svg>">
</head>

<body class="bg-dark">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="#" style="padding-left: 35px"><b>gpuview</b> dashboard</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
                data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false"
                aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
        </div>
    </nav>
    <div class="content-wrapper">
        <div class="container-fluid" style="padding: 0 40px">
            <div class="row">
                % for gpustat in gpustats:
                % for gpu in gpustat.get('gpus', []):
                <div class="col-xl-3 col-md-4 col-sm-6 mb-3">
                    <div class="card text-white {{ gpu.get('flag', '') }} h-100"
                         data-bs-toggle="tooltip"
                         data-bs-placement="top"
                         data-bs-html="true"
                         title="<div class='text-start small'>
<strong>Node:</strong> {{ gpustat.get('hostname', '-') }}<br>
<strong>Device:</strong> {{ gpu.get('name', '-') }}<br>
<strong>Device ID:</strong> {{ gpu.get('index', '-') }}<br>
<strong>Memory:</strong> {{ gpu.get('memory.used', '-') }}/{{ gpu.get('memory.total', '-') }} MB<br>
<strong>Power:</strong> {{ gpu.get('power.draw', '-') }}/{{ gpu.get('enforced.power.limit', '-') }} W<br>
<strong>Temperature:</strong> {{ gpu.get('temperature.gpu', '-') }}°C<br>
<strong>Utilization:</strong> {{ gpu.get('utilization.gpu', '-') }}%<br>
<strong>Processes:</strong> {{ gpu.get('user_processes', '-') }}
</div>">
                        <div class="card-body">
                            <div class="d-flex align-items-center">
                                <div>
                                    <i class="fas fa-server me-2"></i>
                                    <b>{{ gpustat.get('hostname', '-') }}</b>
                                </div>
                            </div>
                            <div class="mt-2">
                                [{{ gpu.get('index', '') }}] {{ gpu.get('name', '-') }}
                            </div>
                        </div>
                        <div class="card-footer text-white small">
                            <div class="row g-1">
                                <div class="col-3">
                                    <i class="fas fa-temperature-three-quarters" aria-hidden="true"></i>
                                    {{ gpu.get('temperature.gpu', '-') }}°C
                                </div>
                                <div class="col-3">
                                    <i class="fas fa-memory" aria-hidden="true"></i>
                                    {{ gpu.get('memory', '-') }}%
                                </div>
                                <div class="col-3">
                                    <i class="fas fa-cogs" aria-hidden="true"></i>
                                    {{ gpu.get('utilization.gpu', '-') }}%
                                </div>
                                <div class="col-3">
                                    <i class="fas fa-users" aria-hidden="true"></i>
                                    {{ gpu.get('users', '-') }}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                % end
                % end
            </div>
            <!-- GPU Stat Card-->
            <div class="card mb-3">
                <div class="card-header">
                    <i class="fas fa-table"></i> All Nodes and GPUs</div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-striped table-bordered" id="dataTable" width="100%">
                            <thead>
                                <tr>
                                    <th scope="col">Node</th>
                                    <th scope="col">Device</th>
                                    <th scope="col">Temp.</th>
                                    <th scope="col">Util.</th>
                                    <th scope="col">Memory Use/Cap</th>
                                    <th scope="col">Power Use/Cap</th>
                                    <th scope="col">User Processes</th>
                                </tr>
                            </thead>
                            <tbody>
                                % for gpustat in gpustats:
                                % for gpu in gpustat.get('gpus', []):
                                <tr class="small">
                                    <th scope="row">{{ gpustat.get('hostname', '-') }}</th>
                                    <td>[{{ gpu.get('index', '') }}] {{ gpu.get('name', '-') }}</td>
                                    <td>{{ gpu.get('temperature.gpu', '-') }}°C</td>
                                    <td>{{ gpu.get('utilization.gpu', '-') }}%</td>
                                    <td>{{ gpu.get('memory', '-') }}% ({{ gpu.get('memory.used', '') }}/{{ gpu.get('memory.total', '-') }})</td>
                                    <td>{{ gpu.get('power.draw', '-') }} / {{ gpu.get('enforced.power.limit', '-') }}</td>
                                    <td>{{ gpu.get('user_processes', '-') }}</td>
                                </tr>
                                % end
                                % end
                            </tbody>
                        </table>
                    </div>
                </div>
                <div class="card-footer small text-muted px-3 py-2">
                    <div class="d-flex justify-content-between align-items-center">
                        <div id="update-timestamp">{{ update_time }}</div>
                        <div class="d-flex align-items-center gap-3">
                            <span id="refresh-status">Auto-refresh: <span class="text-success">ON</span> (every 3s)</span>
                            <a href="#" id="toggle-refresh" class="text-decoration-none small">
                                <i class="fas fa-pause me-1"></i>Pause
                            </a>
                        </div>
                    </div>
                </div>
            </div>

            <div class="row mt-3">
                <div class="col-12">
                    <div class="card bg-light">
                        <div class="card-body p-3">
                            <div class="d-flex align-items-center flex-wrap gap-3">
                                <h6 class="card-title mb-0 me-2"><i class="fas fa-palette me-2"></i>GPU Temperature Legend:</h6>
                                <div class="d-flex flex-wrap gap-2">
                                    <span class="badge rounded-pill bg-danger px-2 py-1">Hot (>75°C)</span>
                                    <span class="badge rounded-pill bg-warning px-2 py-1">Warm (50-75°C)</span>
                                    <span class="badge rounded-pill bg-success px-2 py-1">Normal (25-50°C)</span>
                                    <span class="badge rounded-pill bg-primary px-2 py-1">Cool (<25°C)</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <footer class="py-4 bg-dark">
                <div class="container">
                    <div class="text-center">
                        <small><a href='https://github.com/fgaim/gpuview' class="text-white" style="text-decoration: none"><i class="fab fa-github"></i> fgaim/gpuview | 2025</a></small>
                    </div>
                </div>
            </footer>
        </div>
        <script src="https://code.jquery.com/jquery-3.7.1.min.js"
            integrity="sha256-/JqT3SQfawRcv/BIHPThkBvs0OEvtFFmqPF/lYI/Cxo="
            crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
            integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz"
            crossorigin="anonymous"></script>
        <script src="https://cdn.datatables.net/2.0.3/js/dataTables.min.js"></script>
        <script src="https://cdn.datatables.net/2.0.3/js/dataTables.bootstrap5.min.js"></script>
        <script>
            let dataTable;
            let refreshInterval;
            let isRefreshEnabled = true;

            document.addEventListener('DOMContentLoaded', function() {
                dataTable = new DataTable('#dataTable', {
                    createdRow: function(row, data, dataIndex) {
                        row.classList.add('small');
                    },
                    columnDefs: [
                        { className: 'text-start', targets: '_all' }
                    ]
                });

                var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
                var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
                    return new bootstrap.Tooltip(tooltipTriggerEl);
                });

                const toggleButton = document.getElementById('toggle-refresh');
                const refreshStatus = document.getElementById('refresh-status');

                toggleButton.addEventListener('click', function(e) {
                    e.preventDefault();
                    isRefreshEnabled = !isRefreshEnabled;

                    if (isRefreshEnabled) {
                        refreshInterval = setInterval(updateDashboard, 3000);
                        toggleButton.innerHTML = '<i class="fas fa-pause me-1"></i>Pause';
                        refreshStatus.innerHTML = 'Auto-refresh: <span class="text-success">ON</span> (every 3s)';
                    } else {
                        clearInterval(refreshInterval);
                        toggleButton.innerHTML = '<i class="fas fa-play me-1"></i>Resume';
                        refreshStatus.innerHTML = 'Auto-refresh: <span class="text-danger">PAUSED</span>';
                    }
                });

                // Auto-refresh every 3 seconds
                refreshInterval = setInterval(updateDashboard, 3000);
            });

            async function updateDashboard() {
                try {
                    const response = await fetch('/api/gpustat/all');
                    if (!response.ok) return;

                    const gpustats = await response.json();
                    updateCards(gpustats);
                    updateTable(gpustats);
                    const now = new Date();
                    const timeString = now.toLocaleString() + ' ' + Intl.DateTimeFormat().resolvedOptions().timeZone;
                    document.getElementById('update-timestamp').textContent = `Updated at ${timeString}`;
                } catch (error) {
                    console.log('Auto-refresh failed:', error);
                }
            }

            function updateCards(gpustats) {
                var existingTooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
                existingTooltips.forEach(function(element) {
                    var tooltip = bootstrap.Tooltip.getInstance(element);
                    if (tooltip) {
                        tooltip.dispose();
                    }
                });

                const cardsContainer = document.querySelector('.row');
                cardsContainer.innerHTML = '';

                gpustats.forEach(gpustat => {
                    gpustat.gpus.forEach(gpu => {
                        const temp = gpu['temperature.gpu'];
                        let flag = 'bg-primary';
                        if (temp > 75) flag = 'bg-danger';
                        else if (temp > 50) flag = 'bg-warning';
                        else if (temp > 25) flag = 'bg-success';

                        const cardHtml = `
                            <div class="col-xl-3 col-md-4 col-sm-6 mb-3">
                                <div class="card text-white ${flag} h-100"
                                     data-bs-toggle="tooltip"
                                     data-bs-placement="top"
                                     data-bs-html="true"
                                     title="<div class='text-start small'>
<strong>Node:</strong> ${gpustat.hostname || '-'}<br>
<strong>Device:</strong> ${gpu.name || '-'}, ID: ${gpu.index || '-'}<br>
<strong>Memory:</strong> ${gpu['memory.used'] || '-'} / ${gpu['memory.total'] || '-'} MB<br>
<strong>Power:</strong> ${gpu['power.draw'] || '-'} / ${gpu['enforced.power.limit'] || '-'} W<br>
<strong>Temperature:</strong> ${gpu['temperature.gpu'] || '-'}°C<br>
<strong>Utilization:</strong> ${gpu['utilization.gpu'] || '-'}%<br>
<strong>Processes:</strong> ${gpu['user_processes'] || '-'}
</div>">
                                    <div class="card-body">
                                        <div class="d-flex align-items-center">
                                            <div>
                                                <i class="fas fa-server me-2"></i>
                                                <b>${gpustat.hostname || '-'}</b>
                                            </div>
                                        </div>
                                        <div class="mt-2">
                                            [${gpu.index || ''}] ${gpu.name || '-'}
                                        </div>
                                    </div>
                                    <div class="card-footer text-white small">
                                        <div class="row g-1">
                                            <div class="col-3">
                                                <i class="fas fa-temperature-three-quarters" aria-hidden="true"></i>
                                                ${gpu['temperature.gpu'] || '-'}°C
                                            </div>
                                            <div class="col-3">
                                                <i class="fas fa-memory" aria-hidden="true"></i>
                                                ${gpu.memory || '-'}%
                                            </div>
                                            <div class="col-3">
                                                <i class="fas fa-cogs" aria-hidden="true"></i>
                                                ${gpu['utilization.gpu'] || '-'}%
                                            </div>
                                            <div class="col-3">
                                                <i class="fas fa-users" aria-hidden="true"></i>
                                                ${gpu.users || '-'}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        `;
                        cardsContainer.insertAdjacentHTML('beforeend', cardHtml);
                    });
                });

                var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
                var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
                    return new bootstrap.Tooltip(tooltipTriggerEl);
                });
            }

            function updateTable(gpustats) {
                dataTable.clear();
                const newData = [];
                gpustats.forEach(gpustat => {
                    gpustat.gpus.forEach(gpu => {
                        newData.push([
                            gpustat.hostname || '-',
                            `[${gpu.index || ''}] ${gpu.name || '-'}`,
                            `${gpu['temperature.gpu'] || '-'}°C`,
                            `${gpu['utilization.gpu'] || '-'}%`,
                            `${gpu.memory || '-'}% (${gpu['memory.used'] || ''}/${gpu['memory.total'] || '-'})`,
                            `${gpu['power.draw'] || '-'} / ${gpu['enforced.power.limit'] || '-'}`,
                            gpu['user_processes'] || '-'
                        ]);
                    });
                });
                dataTable.rows.add(newData);
                dataTable.draw(false);
            }
        </script>
    </div>
</body>

</html>
