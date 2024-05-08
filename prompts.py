prompt_3_1_Diagnostico = """
Tu tarea {question} para el documento piscc 2024 en la sección 
3.1 Diagnóstico de la Situación de Seguridad y Convivencia Ciudadana.

Esta sección esta basada en delitos para el municipio de: {municipio}
Siguiendo el siguiente contexto:{context}

Basa el documento en la información de delitos de los ultimos 5 años del municipio {municipio}
detallado en la siguiente sección: {delitos_mes_a_mes}

La secciones anteriores del marco normativo son las siguientes:
3. Diagnóstico de la Situación de Seguridad y Convivencia Ciudadana
3.1 Caracterización de factores de riesgo

Para la redacción de la sección 3.1 se deben tomar en cuenta los siguietes puntos:
- Características geográficas de {municipio}
- Demografía de {municipio}
- Actividades económicas de {municipio}
- Infraestructura de {municipio}
- Instituciones y organizaciones de {municipio}
- Seguridad ciudadana de {municipio}
- Justicia: se sugiere incorporar la capacidad de la Comisaría de Familia, vehículos con los que cuenta,
infraestructura, equipos disponibles para las entidades que hacen parte de esta categoría. para el municipio de {municipio}
- Analisis de la información de delitos mes a mes a detalle: {delitos_mes_a_mes}

IMPORTANTE: El documento generado debe tener un mínimo de 10 párrafos largos.

Redacta solo la Sección 3.1 Análisis de Estadísticas de Seguridad en formato HTML:
"""


prompt_3_2_Diagnostico ="""
Tu tarea es generar solo la sección 3.2 del piscc,
El diagnóstico esta basado en los siguientes delitos para el municipio de: {municipio}

Siguiendo el siguiente contexto:{context}

Indicacion: {question}

Basa tu respuesta en las siguientes información de 
delitos que se registraron en tu municipio: {delitos}

La secciones completas del marco normativo son las siguientes:
3. Diagnóstico de la Situación de Seguridad y Convivencia Ciudadana
3.1 Caracterización de factores de riesgo
3.2 Diagnóstico de delitos
3.3 Diagnóstico de comportamientos contrarios a la convivencia
3.4 Diagnóstico de delitos

Para la redacción de la sección 3.2 toma en cuenta los siguientes preguntas:
- ¿Cuáles son las métricas de delitos en el municipio de: {municipio}?
- ¿Qué efectos tiene dicha delitos en  el municipio de: {municipio}?,
- ¿Cuáles son las acciones adelantadas para mitigar cada delito? 
- ¿Cómo han evolucionado las métricas de este delito en el municipio de: {municipio} a los largo del tiempo

IMPORTANTE: 
- El documento generado debe tener un mínimo de 10 párrafos.
- Toma en cuenta los datos y estadísticas de ue tipos de delitos se 
presentan en en el municipio de: {municipio}.
- Siempre menciona la evolución de las métricas en tasa porcentual.

Redacta solo la Sección 3.2 Diagnóstico de conflictividades en formato HTML:
"""

prompts = { "Diagnostico 3.1": prompt_3_1_Diagnostico, 
            "Diagnostico 3.2": prompt_3_1_Diagnostico,}