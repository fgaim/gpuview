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
<strong>Host:</strong> {{ gpustat.get('hostname', '-') }}<br>
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
                    <i class="fas fa-table"></i> All Hosts and GPUs</div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-striped table-bordered" id="dataTable" width="100%">
                            <thead>
                                <tr>
                                    <th scope="col">Host</th>
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
                <div class="card-footer small text-muted">{{ update_time }}</div>
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
            document.addEventListener('DOMContentLoaded', function() {
                new DataTable('#dataTable');

                var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
                var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
                    return new bootstrap.Tooltip(tooltipTriggerEl);
                });
            });
        </script>
    </div>
</body>

</html>
