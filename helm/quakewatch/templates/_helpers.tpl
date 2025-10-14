{{- define "quakewatch.labels" -}}
app.kubernetes.io/name: {{ include "quakewatch.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/part-of: quakewatch
{{- end }}

{{- define "quakewatch.name" -}}
{{ .Chart.Name }}
{{- end }}
