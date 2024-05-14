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

Describe los delitos de manera general en un solo parrafo: {delitos_mes_a_mes}, junto 
a la tasa por cada mil habitantes {tpcmh}.

Sobre el formato:
- Incluye el uso de negritas al lector a identificar los puntos clave.
- El nombre de la sección es "3. Diagnóstico de la Situación de Seguridad y Convivencia Ciudadana"

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
#Integrar tpcmh
#Integrar grupos étnicos
#Comunidad LGBTQ+

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
<!DOCTYPE html>
<html lang="es">
<body>


<p>En esta sección, se define cómo se financiará y ejecutará el PISCC.  Es fundamental ser realista y detallado para garantizar la viabilidad del plan.</p>

<h2>6.1 Presupuesto Estimado</h2>

<p>Aquí debes detallar el costo total estimado para la implementación del PISCC durante los cuatro años de gobierno.  Debes tener en cuenta los costos de personal, materiales, equipos, capacitación, etc., para cada programa, proyecto y actividad.</p>

<h3>Pasos:</h3>

<ol>
    <li><span class="important">Costear cada programa, proyecto y actividad:</span>
        <ul>
            <li>Identifica todos los recursos necesarios (humanos, materiales, logísticos, etc.).</li>
            <li>Investiga los costos unitarios de cada recurso.</li>
            <li>Calcula el costo total de cada actividad, proyecto y programa.</li>
        </ul>
    </li>
    <li><span class="important">Consolidar los costos:</span>
        <ul>
            <li>Suma los costos de todas las iniciativas para obtener el costo total del PISCC por año.</li>
            <li>Proyecta los costos para los cuatro años de gobierno, considerando posibles incrementos.</li>
        </ul>
    </li>
    <li><span class="important">Presentar el presupuesto en un formato claro y desglosado:</span>
        <ul>
            <li>Utiliza tablas para mostrar el presupuesto por programa, por año, por fuente de financiación, etc.</li>
            <li>Asegúrate de que la información sea fácil de leer y comprender.</li>
        </ul>
    </li>
</ol>

<h3>Ejemplo:</h3>

<table>
    <thead>
        <tr>
            <th>Programa</th>
            <th>Año 1</th>
            <th>Año 2</th>
            <th>Año 3</th>
            <th>Año 4</th>
            <th>Total</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Prevención de la Violencia Juvenil</td>
            <td>$100.000.000</td>
            <td>$120.000.000</td>
            <td>$140.000.000</td>
            <td>$160.000.000</td>
            <td>$520.000.000</td>
        </tr>
        <tr>
            <td>Fortalecimiento del Sistema de Justicia</td>
            <td>$50.000.000</td>
            <td>$60.000.000</td>
            <td>$70.000.000</td>
            <td>$80.000.000</td>
            <td>$260.000.000</td>
        </tr>
        <tr>
            <td><strong>Total</strong></td>
            <td><strong>$150.000.000</strong></td>
            <td><strong>$180.000.000</strong></td>
            <td><strong>$210.000.000</strong></td>
            <td><strong>$240.000.000</strong></td>
            <td><strong>$780.000.000</strong></td>
        </tr>
    </tbody>
</table>

<h2>6.2 Recursos Necesarios</h2>

<p>En esta sección, debes identificar las fuentes de financiación que se utilizarán para cubrir el presupuesto estimado del PISCC.  Es importante explorar todas las opciones disponibles y priorizar las más viables para tu municipio.</p>

<h3>Pasos:</h3>

<ol>
    <li><span class="important">Identificar las fuentes potenciales:</span>
        <ul>
            <li><span class="important">Recursos Propios:</span> Define qué porcentaje del presupuesto municipal se asignará al PISCC. Justifica esta asignación.</li>
            <li><span class="important">FONSET:</span> Describe cómo se utilizarán los recursos del Fondo Territorial de Seguridad y Convivencia Ciudadana (FONSET). Detalla los rubros y montos específicos.</li>
            <li><span class="important">FONSECON:</span> Si planeas solicitar recursos del Fondo Nacional de Seguridad y Convivencia Ciudadana (FONSECON), describe los proyectos que se presentarán y la cofinanciación que aportará el municipio.</li>
            <li><span class="important">Sistema General de Regalías (SGR):</span> Si tu municipio tiene acceso a recursos del SGR, describe los proyectos que se financiarán con estos recursos.</li>
            <li><span class="important">Cooperación Internacional:</span> Explora las posibilidades de cooperación con organismos internacionales, detallando las entidades, los montos y las áreas de apoyo.</li>
            <li><span class="important">Sector Privado:</span> Busca alianzas con empresas privadas que puedan contribuir al PISCC mediante donaciones, inversión social o proyectos conjuntos. </li>
            <li><span class="important">Otros:</span>  Si existen otras fuentes de financiación (convenios interadministrativos, recursos de programas especiales, etc.), descríbelas en detalle.</li>
        </ul>
    </li>
    <li><span class="important">Presentar un plan de financiación:</span>
        <ul>
            <li>Elabora un cuadro que muestre la distribución de los recursos por fuente de financiación y por año. </li>
            <li>Asegúrate de que el plan de financiación sea consistente con el presupuesto estimado y con las metas del PISCC.</li>
        </ul>
    </li>
</ol>

<h3>Ejemplo:</h3>

<table>
    <thead>
        <tr>
            <th>Fuente</th>
            <th>Año 1</th>
            <th>Año 2</th>
            <th>Año 3</th>
            <th>Año 4</th>
            <th>Total</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Recursos Propios</td>
            <td>$50.000.000</td>
            <td>$60.000.000</td>
            <td>$70.000.000</td>
            <td>$80.000.000</td>
            <td>$260.000.000</td>
        </tr>
        <tr>
            <td>FONSET</td>
            <td>$75.000.000</td>
            <td>$90.000.000</td>
            <td>$105.000.000</td>
            <td>$120.000.000</td>
            <td>$390.000.000</td>
        </tr>
        <tr>
            <td>FONSECON</td>
            <td>$25.000.000</td>
            <td>$30.000.000</td>
            <td>$35.000.000</td>
            <td>$40.000.000</td>
            <td>$130.000.000</td>
        </tr>
        <tr>
            <td><strong>Total</strong></td>
            <td><strong>$150.000.000</strong></td>
            <td><strong>$180.000.000</strong></td>
            <td><strong>$210.000.000</strong></td>
            <td><strong>$240.000.000</strong></td>
            <td><strong>$780.000.000</strong></td>
        </tr>
    </tbody>
</table>

<h2>6.3 Asignación de Responsabilidades</h2>

<p>En esta sección, define claramente quiénes serán los responsables de la ejecución del PISCC.  Es importante asignar responsabilidades específicas a cada entidad, dependencia o persona para garantizar una implementación eficiente y coordinada.</p>

<h3>Pasos:</h3>

<ol>
    <li><span class="important">Asignar un responsable principal para cada programa, proyecto y actividad:</span>
        <ul>
            <li>Indica la entidad, dependencia o persona que liderará la ejecución. </li>
            <li>Asegúrate de que el responsable principal tenga la capacidad y los recursos para llevar a cabo sus funciones.</li>
        </ul>
    </li>
    <li><span class="important">Identificar corresponsables:</span>
        <ul>
            <li>Define las entidades o personas que apoyarán al responsable principal.</li>
            <li>Especifica las funciones y responsabilidades de cada corresponsable.</li>
        </ul>
    </li>
    <li><span class="important">Presentar la asignación de responsabilidades en un formato claro:</span>
        <ul>
            <li>Utiliza tablas para mostrar la asignación de responsabilidades, especificando las funciones de cada actor.</li>
            <li>Considera utilizar diagramas para visualizar las relaciones entre los diferentes responsables.</li>
        </ul>
    </li>
</ol>

<h3>Ejemplo:</h3>

<table>
    <thead>
        <tr>
            <th>Programa/Proyecto/Actividad</th>
            <th>Responsable Principal</th>
            <th>Corresponsables</th>
            <th>Funciones del Responsable Principal</th>
            <th>Funciones de los Corresponsables</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Prevención de la Violencia Juvenil</td>
            <td>Secretaría de Educación</td>
            <td>Policía Nacional, ICBF, Secretaría de Cultura</td>
            <td>Diseñar e implementar programas de prevención en instituciones educativas.</td>
            <td>Apoyar la implementación de los programas, brindar capacitación a docentes y padres de familia, promover actividades culturales y deportivas.</td>
        </tr>
        <tr>
            <td>Talleres de Habilidades para la Vida</td>
            <td>ICBF</td>
            <td>Secretaría de Educación, Policía Nacional</td>
            <td>Implementar talleres para jóvenes en riesgo, brindar acompañamiento psicosocial.</td>
            <td>Referir jóvenes a los talleres, apoyar la logística de las actividades, brindar seguridad durante los talleres.</td>
        </tr>
        <tr>
            <td>Fortalecimiento del Sistema de Justicia</td>
            <td>Secretaría de Gobierno</td>
            <td>Fiscalía General de la Nación, Personería Municipal</td>
            <td>Coordinar las acciones del sistema de justicia, gestionar recursos, promover el acceso a la justicia.</td>
            <td>Investigar y judicializar los delitos, atender las denuncias de la comunidad, velar por la protección de los derechos humanos.</td>
        </tr>
    </tbody>
</table>

</body>
</html>
"""

prompt_7_Implementacion = """
<!DOCTYPE html>
<html>
<body>

<p>La implementación es la fase donde las estrategias, programas y proyectos del PISCC cobran vida. Este punto define cómo se llevarán a la práctica las acciones planeadas para mejorar la seguridad y la convivencia en tu municipio.</p>

<h2>7.1 Puesta en Marcha de Estrategias</h2>

<p>En esta sección, se describe el proceso de inicio y ejecución de las estrategias del PISCC.  La clave es detallar las acciones concretas que se llevarán a cabo, los plazos, los responsables y los mecanismos de seguimiento.</p>

<h3>Pasos:</h3>

<ol>
<li><strong>Para cada programa o proyecto, describe:</strong>
<ul>
    <li><strong>Acciones específicas:</strong> Detalla las actividades que se realizarán para implementar la estrategia (ej: talleres de capacitación, campañas de sensibilización, instalación de cámaras de seguridad, mesas de trabajo con la comunidad, etc.).</li>
    <li><strong>Cronograma:</strong> Define el calendario de ejecución de cada acción, especificando fechas de inicio y fin.  Utiliza un diagrama de Gantt o una tabla para visualizar el cronograma.</li>
    <li><strong>Recursos:</strong>  Indica los recursos humanos, materiales y financieros necesarios para cada acción, y cómo se garantizará su disponibilidad. (Ej: presupuesto asignado, personal contratado, equipos disponibles, etc.).</li>
    <li><strong>Mecanismos de seguimiento:</strong>  Establece cómo se monitoreará el progreso de cada acción, los indicadores que se utilizarán (ver punto 5.3 de la Guía PISCC) y la frecuencia del seguimiento (ej: mensual, trimestral, etc.). Define quiénes serán responsables del seguimiento y cómo se reportarán los avances. </li>
</ul>
</li>
</ol>

<h3>Ejemplo:</h3>

<table>
<caption>Programa: Prevención de la Violencia Juvenil</caption>
<thead>
<tr>
    <th>Acción</th>
    <th>Descripción</th>
    <th>Cronograma</th>
    <th>Recursos</th>
    <th>Mecanismos de Seguimiento</th>
</tr>
</thead>
<tbody>
<tr>
    <td>Talleres de Habilidades para la Vida</td>
    <td>Se implementarán talleres para jóvenes en riesgo, en temas como resolución de conflictos, manejo de emociones y toma de decisiones responsables. Los talleres se realizarán en instituciones educativas y espacios comunitarios, con la participación de psicólogos y trabajadores sociales.</td>
    <td>
    <table>
        <thead>
        <tr>
            <th>Mes</th>
            <th>Febrero</th>
            <th>Marzo</th>
            <th>Abril</th>
            <th>...</th>
            <th>Diciembre</th>
        </tr>
        </thead>
        <tbody>
        <tr>
            <td>Talleres de Habilidades para la Vida</td>
            <td>Inicio</td>
            <td>En curso</td>
            <td>En curso</td>
            <td>...</td>
            <td>Finalización</td>
        </tr>
        </tbody>
    </table>
    </td>
    <td>
    <ul>
        <li>Presupuesto: $50.000.000</li>
        <li>Personal: 2 psicólogos, 2 trabajadores sociales</li>
        <li>Materiales: Guías didácticas, material audiovisual</li>
        <li>Espacios: Aulas de clase, salones comunitarios</li>
    </ul>
    </td>
    <td>Seguimiento mensual por parte del ICBF. Se utilizarán indicadores como el número de jóvenes participantes, la satisfacción con los talleres y la reducción de incidentes violentos reportados en las instituciones educativas.  Los avances se reportarán al Comité Territorial de Orden Público trimestralmente.</td>
</tr>
</tbody>
</table>

<h2>7.2 Coordinación Interinstitucional</h2>

<p>Esta sección define cómo se articularán las diferentes entidades, instituciones y actores involucrados en la implementación del PISCC.  La coordinación interinstitucional es crucial para el éxito del plan, ya que permite optimizar recursos, evitar duplicidad de esfuerzos y generar sinergias.</p>

<h3>Pasos:</h3>

<ol>
<li><strong>Define las instancias de coordinación:</strong> 
<ul>
    <li>Describe las instancias de coordinación existentes (ej: Comité Territorial de Orden Público, Consejo de Seguridad) y crea nuevas instancias si es necesario (ej: mesas de trabajo temáticas, comités intersectoriales).</li> 
    <li>Especifica la composición, las funciones, la frecuencia de reuniones y los mecanismos de toma de decisiones de cada instancia.</li>
</ul>
</li>
<li><strong>Establece protocolos de comunicación:</strong> 
<ul>
    <li>Define los canales de comunicación entre las entidades (ej: reuniones presenciales, correos electrónicos, plataforma virtual) y la periodicidad de la comunicación (ej: semanal, quincenal).</li>  
    <li>Desarrolla un sistema de información compartido para facilitar el intercambio de datos y el seguimiento de las acciones.</li>
</ul>
</li>
<li><strong>Promueve la capacitación conjunta:</strong> 
<ul>
    <li>Implementa programas de capacitación para el personal de las diferentes entidades, en temas como:
    <ul>
        <li>Enfoque de seguridad humana y convivencia ciudadana.</li>
        <li>Enfoques diferenciales e interseccionales.</li>
        <li>Prevención del delito y la violencia.</li>
        <li>Mediación y resolución de conflictos.</li>
        <li>Código Nacional de Seguridad y Convivencia Ciudadana (Ley 1801 de 2016).</li>
    </ul>
    </li>
    <li>La capacitación conjunta fortalecerá la comprensión compartida del PISCC y la articulación entre las entidades.</li>
</ul>
</li>
</ol>

<h3>Ejemplo:</h3>

<ul>
<li><strong>Instancia de Coordinación:</strong> Comité Territorial de Orden Público (CTOP)</li>
<li><strong>Composición:</strong> Alcalde (presidente), Secretario de Gobierno (secretario técnico), Comandante de Policía, Comandante del Ejército (si aplica), Director Seccional de Fiscalía, Director del ICBF, Representantes de la comunidad.</li>
<li><strong>Funciones:</strong>
<ul>
    <li>Aprobar el PISCC y el Plan Operativo Anual de Inversiones (POAI).</li>
    <li>Hacer seguimiento a la implementación del PISCC.</li>
    <li>Tomar decisiones sobre la asignación de recursos del FONSET.</li>
    <li>Resolver conflictos interinstitucionales.</li>
    <li>Evaluar los avances y resultados del PISCC.</li>
</ul>
</li>
<li><strong>Frecuencia de Reuniones:</strong> Mensual (ordinaria) y cuando sea necesario (extraordinaria).</li>
<li><strong>Mecanismos de Toma de Decisiones:</strong> Consenso, votación (en caso de ser necesario).</li>
<li><strong>Protocolo de Comunicación:</strong> Se utilizará una plataforma virtual para compartir información, documentos y actas de las reuniones.  Se realizarán reuniones presenciales mensuales y se mantendrá comunicación constante vía correo electrónico para asuntos urgentes.</li>
</ul>

<h2>7.3 Evaluación de Avances</h2>

<p>Esta sección define cómo se evaluará el progreso de la implementación del PISCC.  La evaluación debe ser periódica, rigurosa y participativa, y debe permitir identificar los logros, las dificultades y las áreas de mejora.</p>

<h3>Pasos:</h3>

<ol>
<li><strong>Define los indicadores de seguimiento y evaluación:</strong> 
<ul>
    <li>Utiliza los indicadores definidos en el punto 5.3 de la Guía PISCC. </li>
    <li>Asegúrate de que los indicadores sean relevantes, medibles, alcanzables, relevantes y con límite de tiempo (SMART).</li>
</ul>
</li>
<li><strong>Establece la periodicidad de la evaluación:</strong> 
<ul>
    <li>Define la frecuencia de la evaluación (ej: trimestral, semestral, anual).</li>
</ul>
</li>
<li><strong>Desarrolla herramientas de evaluación:</strong> 
<ul>
    <li>Crea herramientas para recolectar datos y analizar la información (ej: encuestas de percepción ciudadana, análisis de estadísticas delictivas, informes de las entidades responsables, grupos focales con la comunidad, etc.).</li>
</ul>
</li>
<li><strong>Implementa mecanismos de retroalimentación:</strong> 
<ul>
    <li>Establece mecanismos para que las entidades responsables, la comunidad y otros actores puedan brindar retroalimentación sobre la implementación del PISCC.  La retroalimentación permitirá realizar ajustes y mejoras al plan de forma oportuna.</li>
</ul>
</li>
<li><strong>Socializa los resultados de la evaluación:</strong> 
<ul>
    <li>Los resultados de la evaluación deben ser comunicados a las entidades responsables, al Comité Territorial de Orden Público, al Concejo Municipal y a la comunidad.  La socialización de los resultados promoverá la transparencia, la rendición de cuentas y la participación ciudadana.</li>
</ul>
</li>
</ol>

<h3>Ejemplo:</h3>

<ul>
<li><strong>Indicadores de Seguimiento:</strong>
<ul>
    <li>Tasa de homicidios por cada 100.000 habitantes.</li>
    <li>Número de denuncias por violencia intrafamiliar.</li>
    <li>Percepción de seguridad ciudadana (encuesta).</li>
    <li>Número de jóvenes participantes en programas de prevención.</li>
</ul>
</li>
<li><strong>Periodicidad de la Evaluación:</strong> Trimestral.</li>
<li><strong>Herramientas de Evaluación:</strong>
<ul>
    <li>Análisis de estadísticas delictivas (SIEDCO).</li>
    <li>Encuesta de percepción de seguridad ciudadana.</li>
    <li>Informes de las entidades responsables de los programas y proyectos.</li>
    <li>Grupos focales con la comunidad.</li>
</ul>
</li>
<li><strong>Mecanismos de Retroalimentación:</strong>
<ul>
    <li>Buzón de sugerencias en la página web de la Alcaldía.</li>
    <li>Espacios de diálogo con la comunidad en las reuniones del CTOP.</li>
    <li>Reuniones con las entidades responsables para analizar los informes de seguimiento.</li>
</ul>
</li>
<li><strong>Socialización de Resultados:</strong>
<ul>
    <li>Se presentará un informe trimestral al CTOP y al Concejo Municipal.</li> 
    <li>Se publicarán los resultados de la encuesta de percepción de seguridad en la página web de la Alcaldía.</li>
    <li>Se realizarán reuniones con la comunidad para socializar los avances y recibir retroalimentación.</li>
</ul>
</li>
</ul>

<h3>Recomendaciones Adicionales:</h3>

<ul>
<li><strong>Flexibilidad:</strong> La implementación del PISCC debe ser flexible para adaptarse a las dinámicas cambiantes de la seguridad y la convivencia en el municipio.</li>
<li><strong>Comunicación efectiva:</strong>  Mantén una comunicación fluida y transparente con todas las entidades, instituciones y actores involucrados.</li>
<li><strong>Rendición de cuentas:</strong>  Informa a la comunidad sobre los avances y resultados del PISCC de forma regular.</li>
<li><strong>Gestión del conocimiento:</strong> Documenta las lecciones aprendidas y las buenas prácticas para fortalecer la implementación del PISCC en el futuro.</li>
</ul>

<p>¡Con una implementación efectiva, el PISCC podrá contribuir significativamente a la construcción de un municipio más seguro y con mejor convivencia para todos!</p>

</body>
</html>
"""

prompt_8_Seguimiento = """

<p>El seguimiento y evaluación utilizando la herramienta de seguimiento es crucial para asegurar que el PISCC esté logrando sus objetivos y generando un impacto positivo en la seguridad y la convivencia.  Esta sección describe cómo se monitoreará el progreso del plan, se evaluará su impacto y se realizarán ajustes para mejorar su eficacia.</p>

<h3>8.1 Monitoreo de Indicadores de Gestión</h3>

<p>El monitoreo se centra en el seguimiento regular de los indicadores de gestión (o de proceso), que miden la eficiencia y eficacia de la implementación del PISCC. Estos indicadores nos permiten saber si las acciones se están ejecutando según lo planeado y si se están utilizando los recursos de forma adecuada.</p>

<h4>Pasos:</h4>

<ol>
<li>
<b>Define los indicadores de gestión:</b>
<ul>
    <li>Selecciona los indicadores que te permitirán monitorear el progreso de la implementación de cada programa, proyecto o actividad.</li>
    <li>Elige indicadores que sean específicos, medibles, alcanzables, relevantes y con límite de tiempo (SMART).</li>
    <li>
    Algunos ejemplos de indicadores de gestión podrían ser:
    <ul>
        <li>Número de talleres de capacitación realizados.</li>
        <li>Porcentaje de ejecución presupuestal.</li>
        <li>Número de cámaras de seguridad instaladas.</li>
        <li>Cantidad de reuniones del Comité Territorial de Orden Público.</li>
    </ul>
    </li>
</ul>
</li>
<li>
<b>Establece la periodicidad del monitoreo:</b>
<ul>
    <li>Define con qué frecuencia se recopilarán los datos y se analizarán los indicadores (ej: mensual, trimestral).</li>
    <li>Considera la disponibilidad de datos y la necesidad de información oportuna para la toma de decisiones.</li>
</ul>
</li>
<li>
<b>Desarrolla herramientas de monitoreo:</b>
<ul>
    <li>Crea herramientas para facilitar la recolección, análisis y visualización de los datos (ej: bases de datos, hojas de cálculo, tableros de control).</li>
    <li>Utiliza herramientas que permitan generar informes de seguimiento de forma clara y concisa.</li>
    <li>El módulo PISCC del SisPT es una herramienta útil para el monitoreo.</li>
</ul>
</li>
<li>
<b>Asigna responsabilidades:</b>
<ul>
    <li>Define quiénes serán responsables de recopilar los datos, analizar los indicadores y generar los informes de seguimiento.</li>
    <li>Asegúrate de que los responsables tengan la capacidad y los recursos para llevar a cabo sus funciones.</li>
</ul>
</li>
<li>
<b>Socializa los resultados del monitoreo:</b>
<ul>
    <li>Comparte los informes de seguimiento con las entidades responsables, el Comité Territorial de Orden Público, el Concejo Municipal y la comunidad.</li>
    <li>La socialización de los resultados promoverá la transparencia, la rendición de cuentas y la participación ciudadana.</li>
</ul>
</li>
</ol>

<h3>8.2 Evaluación de Impacto</h3>

<p>La evaluación de impacto se centra en determinar los efectos del PISCC en la seguridad y la convivencia del municipio.  Se busca medir si el plan está logrando los resultados esperados y si está generando cambios positivos en la calidad de vida de la comunidad.</p>

<h4>Pasos:</h4>

<ol>
<li>
<b>Define los indicadores de impacto:</b>
<ul>
    <li>Selecciona los indicadores que te permitirán medir los efectos del PISCC en las problemáticas priorizadas (ej: reducción de la tasa de homicidios, disminución de la violencia intrafamiliar, mejora en la percepción de seguridad).</li>
    <li>Recuerda que los indicadores de impacto deben estar alineados con los objetivos del PISCC.</li>
</ul>
</li>
<li>
<b>Establece la línea de base:</b>
<ul>
    <li>Recopila datos sobre la situación de la seguridad y la convivencia en el municipio antes de la implementación del PISCC.  Esta información te servirá como punto de referencia para comparar los resultados.</li>
</ul>
</li>
<li>
<b>Elige una metodología de evaluación:</b>
<ul>
    <li>Selecciona una metodología de evaluación que se ajuste a las características de tu PISCC y a los recursos disponibles.  Puedes considerar métodos cuantitativos (ej: análisis de estadísticas), cualitativos (ej: entrevistas, grupos focales) o mixtos.</li>
</ul>
</li>
<li>
<b>Realiza la evaluación de impacto:</b>
<ul>
    <li>Recopila datos sobre los indicadores de impacto después de un periodo determinado de implementación del PISCC (ej: un año, dos años).</li>
    <li>Analiza los datos y compara los resultados con la línea de base para determinar si el plan está teniendo un impacto positivo.</li>
</ul>
</li>
<li>
<b>Socializa los resultados de la evaluación de impacto:</b>
<ul>
    <li>Presenta los resultados de la evaluación a las entidades responsables, al Comité Territorial de Orden Público, al Concejo Municipal y a la comunidad.</li>
    <li>Utiliza los resultados de la evaluación para tomar decisiones informadas sobre la continuidad, los ajustes o la reformulación del PISCC.</li>
</ul>
</li>
</ol>

<h3>8.3 Ajustes y Mejoras Continuas</h3>

<p>El seguimiento y evaluación deben servir para identificar las fortalezas y debilidades del PISCC, y para realizar ajustes y mejoras que permitan optimizar su implementación y maximizar su impacto.</p>

<h4>Pasos:</h4>

<ol>
<li>
<b>Analiza los resultados del monitoreo y la evaluación:</b>
<ul>
    <li>Identifica las acciones que están funcionando bien y las que presentan dificultades.</li>
    <li>Analiza las causas de los problemas y busca soluciones.</li>
</ul>
</li>
<li>
<b>Propón ajustes y mejoras al PISCC:</b>
<ul>
    <li>Realiza cambios en las acciones, los cronogramas, los recursos o los responsables, según sea necesario.</li>
    <li>Considera la retroalimentación de las entidades responsables, la comunidad y otros actores.</li>
</ul>
</li>
<li>
<b>Implementa los ajustes y mejoras:</b>
<ul>
<li>Actualiza el PISCC y el Plan Operativo Anual de Inversiones (POAI) con los cambios aprobados.</li>
<li>Comunica los ajustes a las entidades responsables y a la comunidad.</li>
</ul>
</li>
<li>
<b>Continúa el monitoreo y la evaluación:</b>
<ul>
<li>Monitorea los indicadores de gestión y evalúa el impacto del PISCC de forma regular.</li>
<li>Utiliza la información del seguimiento y evaluación para realizar nuevos ajustes y mejoras de forma continua.</li>
</ul>
</li>
</ol>

<p>Recuerda que el PISCC es un instrumento dinámico que debe adaptarse a las necesidades cambiantes del municipio.  El seguimiento y evaluación, junto con la implementación de ajustes y mejoras, te permitirán mantener el plan actualizado y eficaz para la construcción de un municipio más seguro y con mejor conv
"""

prompt_9_Anexos = """
<!DOCTYPE html>
<html>
<body>

<p>Los anexos del PISCC son una sección importante para proporcionar información detallada y complementaria que no se incluye en el cuerpo principal del plan. Sirven para sustentar las decisiones tomadas, evidenciar el trabajo realizado y facilitar la consulta de información relevante.</p>

<h2>9.1 Documentos de Apoyo</h2>

<p>En esta subsección, se incluyen documentos que sirvieron de base para la elaboración del PISCC, como estudios, diagnósticos, análisis, planes y políticas.</p>

<h3>Ejemplos de documentos que puedes incluir:</h3>
<ul>
<li><strong>Diagnóstico de seguridad y convivencia:</strong> El diagnóstico realizado para identificar las problemáticas, los factores de riesgo y las necesidades del municipio (ver punto 3 de la Guía PISCC).</li>
<li><strong>Plan de Desarrollo Municipal (PDM):</strong>  El plan de desarrollo del municipio, en el que se establecen las metas y estrategias de desarrollo territorial.</li>
<li><strong>Planes de acción sectoriales:</strong> Planes de acción de las diferentes secretarías o entidades del municipio que tienen relación con la seguridad y la convivencia ciudadana (ej: Secretaría de Gobierno, Secretaría de Educación, Secretaría de Salud, etc.).</li>
<li><strong>Políticas nacionales y departamentales:</strong> Políticas de seguridad y convivencia ciudadana del nivel nacional y departamental que se consideraron en la elaboración del PISCC.</li>
<li><strong>Estudios y análisis:</strong> Estudios, investigaciones o análisis sobre la seguridad y la convivencia en el municipio o en contextos similares.</li>
<li><strong>Mapas y cartografías:</strong>  Mapas que muestren la distribución geográfica de las problemáticas de seguridad y convivencia, los puntos críticos, los recursos disponibles, etc.</li>
<li><strong>Actas de reuniones:</strong> Actas de las reuniones del Comité Territorial de Orden Público u otras instancias de coordinación en las que se discutió y aprobó el PISCC.</li>
</ul>

<h2>9.2 Informes de Seguimiento</h2>

<p>En esta subsección, se incluyen los informes de seguimiento a la implementación del PISCC.  Estos informes deben mostrar el progreso de las acciones, los resultados obtenidos y las dificultades encontradas.</p>

<h3>Ejemplos de informes que puedes incluir:</h3>
<ul>
<li><strong>Informes trimestrales o semestrales:</strong>  Informes que muestren el avance de la implementación del PISCC, con base en los indicadores de gestión y de impacto.</li>
<li><strong>Informes de evaluación:</strong> Informes de las evaluaciones de impacto realizadas, que muestren los efectos del PISCC en la seguridad y la convivencia del municipio.</li>
<li><strong>Informes de las entidades responsables:</strong>  Informes de seguimiento elaborados por las diferentes entidades responsables de la implementación de los programas y proyectos del PISCC.</li>
</ul>

<h2>9.3 Otros Recursos Relevantes</h2>

<p>En esta subsección, se incluye cualquier otro recurso que se considere relevante para la comprensión o la implementación del PISCC.</p>

<h3>Ejemplos de recursos que puedes incluir:</h3>
<ul>
<li><strong>Base de datos de contactos:</strong>  Información de contacto de las entidades, instituciones y personas clave para la implementación del PISCC.</li>
<li><strong>Material de capacitación:</strong>  Presentaciones, guías, manuales u otros materiales utilizados en las capacitaciones sobre el PISCC.</li>
<li><strong>Material de difusión:</strong>  Folletos, carteles, videos u otros materiales de comunicación utilizados para difundir el PISCC a la comunidad.</li>
<li><strong>Enlaces a recursos externos:</strong>  Enlaces a páginas web, documentos o bases de datos relevantes para la seguridad y la convivencia ciudadana.</li>
</ul>

<p>Recuerda que los anexos deben estar organizados de forma clara y ordenada, y deben ser fácilmente accesibles para los usuarios del PISCC.</p>

</body>
</html>
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