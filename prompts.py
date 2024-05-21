prompt_1_Introduccion = """
Tu tarea es {question} para el documento piscc 2024.

Esta sección esta basada en delitos para el municipio de: {municipio}
Siguiendo el siguiente contexto:{context} para identificar todos los factores de riesgo que pueden conllevar 
a delitos en el municipio.

Basa el documento en la información de delitos de los ultimos 5 años del municipio {municipio}
detallado en la siguiente sección: {delitos_mes_a_mes}

Para la redacción de la sección 1. debes tomar los siguientes puntos:
- Describe de manera general los retos frente delitos mas frecuentes la ultima temporada.
- Para qué servirá el piscc en el municipio de {municipio}.
- ¿Cuál es el compromiso la realización del piscc 2024-2027?
- ¿Cuál será el resultado del proceso?

Sobre el formato:
- Incluye el uso de negritas, cursivas y listas para ayudar al lector a identificar los puntos clave.
- Establece Objetivo general y Objetivos específicos basados en los delitos de manera general y el contexto.

IMPORTANTE: 
- El documento generado debe tener un mínimo de 10 párrafos largos.
- No incluyas un párrafo de resumen de la sección.
- No incluyas el subtítulo de la sección, solo el contenido.

Redacta solo la Sección 1. Introducción en formato HTML:
"""

prompt_2_Introduccion = """
Tu tarea es {question} para el documento piscc 2024 enlazando la sección previa: {seccion_context}.

Esta se enfoca en el marco legislativo que respalda la creación de PISCC y su objetivo,
Siguiendo el siguiente contexto:{context}, cita las leyes de importancia para programa
el plan integral de ocnvivencia y seguridad ciduadana.

Toma en cuneta los delitos de los ultimos 5 años del municipio {municipio} 
detallado en la siguiente sección: {delitos_mes_a_mes} par avalidar el marco normativo.

Para la redacción de la sección 2. debes tomar los siguientes puntos:
- Lineamiento del Plan Nacional de Desarrollo del Gobierno nacional co nel piscc.
- Incluye enfoques diferenciales e interseccionales según las características y necesidades de la 
población en la entidad territorial segun  la información de:
    - Características geográficas de {municipio}
    - Demografía de {municipio}

Sobre el formato:
- Incluye el uso de negritas, cursivas para ayudar al lector a identificar los puntos clave.
- No incluyas el subtítulo de la sección, solo el contenido.

IMPORTANTE: 
- El documento generado debe tener un mínimo de 10 párrafos largos.
- No incluyas un párrafo de resumen de la sección.

Redacta solo la Sección 2. en formato HTML:
"""
#Se recomienda contar con el detalle del municipio para datos de género o información de 
#la comunidad LGBTQ+ en el municipio.

prompt_3_Diagnostico = """
Tu tarea es {question} para el documento piscc 2024 enlazando la sección previa: {seccion_context}.

Esta sección esta basada en la introducción a datos sobre el municipio de: {municipio}
Siguiendo el siguiente contexto:{context} describe la información del municipio, del alcalde y sus
principales funciones y resposnabilidad en la elaboración del piscc.

Describe los delitos de manera detallada: {delitos_mes_a_mes}, junto 
a la tasa por cada mil habitantes {tpcmh}.

Sobre el formato:
- Incluye el uso de negritas al lector a identificar los puntos clave.
- El nombre de la sección es "3. Diagnóstico de la Situación de Seguridad y Convivencia Ciudadana"
- Siempre incluye datos numéricos.

IMPORTANTE: 
- El documento generado debe tener un mínimo de 5 párrafos largos.
- No incluyas un párrafo de resumen de la sección.
- No incluyas el subtítulo de la sección, solo el contenido.

Redacta solo la Sección 3 en formato HTML:
"""
#¿Cómo saber cuál es el alcalde alctual de cada municipio?

prompt_3_1_Diagnostico = """
Tu tarea es {question} para el documento piscc 2024 enlazando la sección previa: {seccion_context}.

Esta sección esta basada en delitos para el municipio de: {municipio}
Siguiendo el siguiente contexto:{context} para identificar todos los factores de riesgo que pueden conllevar 
a delitos en el municipio.

Basa el documento en la información de delitos de los ultimos 5 años del municipio {municipio}
detallado en la siguiente sección: {delitos_mes_a_mes} y en la tasa por cada mil habitantes {tpcmh}.

Para la redacción de la sección 3.1 se debe redactar la directa relación de violencia y delitos 
descritos con los siguientes puntos:
- Características geográficas de {municipio}
- Demografía de {municipio}
- Actividades económicas de {municipio}
- Infraestructura de {municipio}
- Instituciones y organizaciones de {municipio}
- Seguridad ciudadana de {municipio}
- Justicia: se sugiere incorporar la capacidad de la Comisaría de Familia, vehículos con los que cuenta,
infraestructura, equipos disponibles para las entidades que hacen parte de esta categoría. para el municipio de {municipio}

Sobre el formato:
- No incluyas un párrafo de resumen de la sección.
- Siempre incluye datos numéricos.

IMPORTANTE: 
- El documento generado debe tener un mínimo de 10 párrafos largos.
- No incluyas el subtítulo de la sección, solo el contenido.

Redacta solo la Sección 3.1 Análisis de Estadísticas de Seguridad en formato HTML:
"""

prompt_3_2_Diagnostico ="""
Tu tarea es {question} para el documento piscc 2024 enlazando la sección previa: {seccion_context}.

La sección 3.2 del municipio: {municipio} Sigue el siguiente contexto:{context}
Tomando en cuenta los delitos registrados: {delitos_mes_a_mes} y la tasa por cada mil habitantes {tpcmh}.
la seccion se redacta siguiendo los siguientes puntos:
1. Información general del municipio {municipio}.
2. Antecedentes históricos del municipio {municipio} que hayan impactado los temas de acceso a la justicia.
3. Análisis del contexto territorial (población, calidad de vida, condiciones económicas y políticas, entre 
otras).
4. Análisis de conflictividad del municipio {municipio} (causas y efectos de las conflictividades, barreras de 
acceso a la justicia, tipologías de conflicto, entre otros).
5. Mapeo de actores (organizaciones comunitarias, oferta de justicia y convivencia, entidades del 
orden local, entre otros).

Sobre el formato:
- Incluye el uso de negritas y cursivas para ayudar al lector a identificar los puntos clave.
- No incluyas un párrafo de resumen de la sección.
- No incluyas el subtítulo de la sección, solo el contenido.
- Incluye un análsis detendencias estádisticas entre los delitos de los últimos 5 años.
- Siempre incluye datos numéricos.

IMPORTANTE: El documento generado debe tener un mínimo de 10 párrafos largos.
Redacta 3.2 Diagnóstico de conflictividades. en formato HTML:
"""

prompt_3_3_Diagnostico ="""
Tu tarea es {question} para el documento piscc 2024 continuando a la sección previa: {seccion_context}.

La sección 3.3 del municipio: {municipio} Sigue el siguiente contexto:{context}

la seccion se redacta siguiendo los siguientes puntos:
- Principales comportamientos contrarios a la convivencia. 
- Número y tipo de comportamientos contrarios a la convivencia que afectan a personas de 
determinados grupos étnicos, así como a personas con orientaciones sexuales e identidades de género diversas.

Sobre el formato:
- Incluye el uso de negritas, cursivas y listas para ayudar al lector a identificar los puntos clave.
- Siempre incluye datos numéricos.

IMPORTANTE: 
- No incluyas un párrafo de resumen de la sección.
- Redacta 3 párrafos para cada sección.
- No incluyas el subtítulo de la sección, solo el contenido.

Redacta 3.3 Diagnóstico de comportamientos contrarios a la convivencia. en formato HTML:
"""

prompt_3_4_Diagnostico ="""
Tu tarea es {question} para el documento piscc 2024 continuando a la sección previa: {seccion_context}.

La sección 3.4 del municipio: {municipio} Sigue el siguiente contexto:{context}

La seccion se redacta siguiendo los siguientes puntos:
- Número y tipo de comportamientos contrarios a la convivencia que afectan a personas de 
determinados grupos étnicos, así como a personas con orientaciones sexuales e identidades de género diversas.
- Detalle estadístico minucioso sobre los delitos en el municipio de {municipio} en los últimos 
5 años detallados en la sección: {delitos_mes_a_mes} y tpcmh detallados en: {tpcmh}.


IMPORTANTE: 
- El documento generado debe tener un mínimo de 20 párrafos largos.
- No incluyas un párrafo de resumen de la sección.
- No incluyas el subtítulo de la sección, solo el contenido.

Redacta 3.4 Diagnóstico de delitos. en formato HTML:
"""

prompt_4_Focalizacion ="""
Tu tarea es {question} para el documento piscc 2024 continuando a la sección previa: {seccion_context}.

La sección 4 del municipio: {municipio} Sigue el siguiente contexto:{context} para la
redacción de los siguientes puntos:
4. Focalización y Priorización para la Planeación
4.1 Identificación de Zonas Críticas
4.2 Definición de Grupos de Población Vulnerables
4.3 Priorización de Problemas a Abordar

La sección se basa en los delitos: {delitos_mes_a_mes} en los últimos 5 años. y a partir de estos definiendo:
- Selecición de los 3 delitos más frecuentes en el municipio de {municipio} los últimos 3 años.
- Criterios que se utilizaron para seleccionar las problematicas (delitos).
- Marco legal que respalda la focalización y priorización de los delitos.

Sobre el formato:
- Incluye un poco de negritas, cursivas y listas para ayudar al lector a identificar los puntos clave.
- Incluye una tabla donde se idnetifiquen los 3 delitos seleccionados y los puntos de selección de cada uno asignando un puntaje de 1 a 10
según los puntos extraídos de las politicas extraidas del contexto: {context}.
- Incluye las estrategias de manera general de intervención para cada uno de los delitos seleccionados que se mencionan en el contexto.

IMPORTANTE: 
- El documento generado debe tener un mínimo de 20 párrafos largos.
- No incluyas un párrafo de resumen de la sección.
- Solo para la sección 4. no incluyas el nombre de la sección, solo el contenido.
- Para los subtitulos 4.1 4.2 y 4.3 redacta 5 párrafos para cada uno.
- Para los subtitulos 4.1 4.2 y 4.3 incluye sus titulos y su contenido.

Redacta parafos extensos de las secciones en formato HTML:
"""

prompt_5_Formulacion = """ 
Tu tarea es {question} para el documento piscc 2024 continuando a la sección previa: {seccion_context}.

La sección 5 del municipio: {municipio} Sigue el siguiente contexto:{context} para la
redacción de los siguientes puntos:
5. Formulación Estratégica del PISCC
5.1 Estrategias de Intervención

La sección se basa en los delitos seleccionados en {seccion_context} de los delitos detallados el {delitos_mes_a_mes},
a partir estos detalla lo siguiente::
- Detalle de cada estrategias de intervención para cada uno de los delitos seleccionados.
- Justificación de la selección de las estrategias de intervención.
- Relación de las estrategias de intervención con los objetivos del PISCC.
- Relación de las estrategias de intervención con los resultados esperados del PISCC.
- Relación de las estrategias de intervención con los indicadores de gestión y resultados del PISCC.

Sobre el formato:
- Incluye cursivas para ayudar al lector a identificar los puntos clave.
- Incluye la justificación de responsabilidad del alcalde en la implementación de las estrategias de intervención.

IMPORTANTE: 
- El documento generado debe tener un mínimo de 10 párrafos extensos.
- No incluyas un párrafo de resumen de la sección.
- No aumentes otras secciones
- Solo para la sección 5. no incluyas el nombre de la sección, solo el contenido.
- Para los subtitulos 5.1 incluye sus titulos y su contenido.

Redacta parafos extensos de las secciones en formato HTML:
"""

prompt_6_Financiamiento = """ 
"Tu tarea es {question} para el documento piscc 2024 continuando a la sección previa: {seccion_context}.

La sección 6 del municipio: {municipio} Sigue el siguiente contexto:{context} para la redacción de los siguientes puntos:
6. Planeación Financiera y Operativa
6.1 Presupuesto Estimado
6.2 Recursos Necesarios
6.3 Asignación de Responsabilidades

La sección se basa en los delitos seleccionados en {seccion_context} de los delitos detallados el {delitos_mes_a_mes}, a partir de estos detalla lo siguiente:
- Detalle de cada estrategia de intervención para cada uno de los delitos seleccionados.
- Justificación de la selección de las estrategias de intervención.
- Relación de las estrategias de intervención con los objetivos del PISCC.
- Explicacion de las tablas de presupuesto y un ejemplo de la tabla.

Sobre el formato:
- Incluye cursivas para ayudar al lector a identificar los puntos clave.
- No incluyas presupuesto, solo la explicación de como llenar las tablas.
- Solo para la sección 6. no incluyas el nombre de la sección, solo el contenido.
- Incluye los subtitulos 6.1 6.2 y 6.3.

IMPORTANTE: 
- El documento generado debe tener un mínimo de 10 párrafos extensos.
- No incluyas un párrafo de resumen de la sección.
- No aumentes otras secciones.
- Incluye tablas que expliquen como llenar en base al presupuesto.

Redacta párrafos extensos de las secciones en formato HTML:"""

prompt_7_Implementacion = """
Tu tarea es {question} para el documento piscc 2024 continuando a la sección previa: {seccion_context}.

La sección 7 del municipio: {municipio} Sigue el siguiente contexto:{context} para la
redacción de los siguientes puntos:
7. Implementación del PISCC
7.1 Puesta en Marcha de Estrategias
7.2 Coordinación Interinstitucional
7.3 Evaluación de Avances

La sección se basa en los delitos seleccionados en {seccion_context} de los delitos detallados el {delitos_mes_a_mes},
a partir estos detalla lo siguiente::
- Cómo Poner en marcha las estrategias del PISCC paraasegurar la coordinación entre las instituciones, 
y monitorear el progreso de la implementación.
- Crea un cronograma, asigna recursos, planifica capacitaciones, desarrolla un plan de comunicación,
y establece un proceso para monitorear la implementación.
- Define roles y responsabilidades, crea comités de seguimiento, considera plataformas de colaboración, y busca convenios de colaboración.
- Define indicadores de implementación, realiza evaluaciones de procesos, y elabora informes de avance.

Sobre el formato:
- Incluye cursivas para ayudar al lector a identificar los puntos clave.
- Incluye la justificación de responsabilidad del alcalde en la implementación de las estrategias de intervención.
- Solo para la sección 7. no incluyas el nombre de la sección, solo el contenido.
- Incluye los subtitulos 7.1 7.2 y 7.3.

IMPORTANTE: 
- El documento generado debe tener un mínimo de 10 párrafos extensos.
- No incluyas un párrafo de resumen de la sección.
- No aumentes otras secciones.

Redacta parafos extensos de las secciones en formato HTML:
"""

prompt_8_Seguimiento = """
Tu tarea es {question} para el documento piscc 2024 continuando a la sección previa: {seccion_context}.

La sección 8 del municipio: {municipio} Sigue el siguiente contexto:{context} para la
redacción de los siguientes puntos:
8. Seguimiento y Evaluación del PISCC
8.1 Monitoreo de Indicadores de Gestión
8.2 Evaluación de Impacto
8.3 Ajustes y Mejoras Continuas

La sección se basa en los delitos seleccionados en {seccion_context} de los delitos detallados el {delitos_mes_a_mes},
a partir estos detalla lo siguiente::
- Establece la frecuencia de seguimiento (mensual, trimestral, etc.).
- Especifica las herramientas (hojas de cálculo, SisPT, etc.).
- Describe los sistemas de registro de información que es el "creador de PISCC con inteligencia artificial".
- Explica cómo se analizarán los datos y se crearán informes.
- Define el objetivo principal de la evaluación (medir resultados, identificar efectos, obtener evidencia).

Sobre el formato:
- Incluye cursivas para ayudar al lector a identificar los puntos clave.
- Incluye la justificación de responsabilidad del alcalde en la implementación de las estrategias de intervención.
- Solo para la sección 8. no incluyas el nombre de la sección, solo el contenido.
- Incluye los subtitulos 8.1 8.2 y 8.3.

IMPORTANTE: 
- El documento generado debe tener un mínimo de 10 párrafos extensos.
- No incluyas un párrafo de resumen de la sección.
- No aumentes otras secciones

Redacta parafos extensos de las secciones en formato HTML:
"""

prompt_9_Anexos = """
Tu tarea es {question} para el documento piscc 2024 continuando a la sección previa: {seccion_context}.

La sección 9 del municipio: {municipio} Sigue el siguiente contexto:{context} para la
redacción de los siguientes puntos:
9.Anexos
9.1 Documentos de Apoyo
9.2 Informes de Seguimiento
9.3 Otros Recursos Relevantes de Apoyo
9.2 Informes de Seguimiento
9.3 Otros Recursos Relevantes

La sección se basa en apoyar con documentación adicional para el PISCC, a partir estos detalla lo siguiente:
- Marco legal, políticas públicas, Plan Nacional de Desarrollo, estudios y diagnósticos.
- Informes de monitoreo, evaluaciones de procesos, evaluaciones de impacto.
- Otros Recursos Relevantes: Mapas, gráficos, tablas, material de comunicación, recursos de capacitación.

Sobre el formato:
- Incluye cursivas para ayudar al lector a identificar los puntos clave.
- Solo para la sección 9. no incluyas el nombre de la sección, solo el contenido.
- Incluye los subtitulos 9.1 9.2 y 9.3.

IMPORTANTE: 
- El documento generado debe tener un mínimo de 10 párrafos extensos.
- No incluyas un párrafo de resumen de la sección.
- No aumentes otras secciones

Redacta parafos extensos de las secciones en formato HTML:
"""

prompts_dict = { "1 Introducción": prompt_1_Introduccion,
                "2 Marco Normativo": prompt_2_Introduccion,
                "3 Diagnostico 3.1": prompt_3_1_Diagnostico, 
            "3 Diagnostico 3.2": prompt_3_2_Diagnostico,
            "3 Diagnostico 3.3": prompt_3_3_Diagnostico,
            "3 Diagnostico 3.4": prompt_3_4_Diagnostico,
            "4 Focalización" : prompt_4_Focalizacion,
            "5 Formulación" : prompt_5_Formulacion,
            "6 Financiamiento" : prompt_6_Financiamiento,
            "7 Implementación" : prompt_7_Implementacion,
            "8 Seguimiento" : prompt_8_Seguimiento,
            "9 Anexos" : prompt_9_Anexos
            }