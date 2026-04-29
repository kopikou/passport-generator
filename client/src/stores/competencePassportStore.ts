import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from 'boot/axios'
import { LocalStorage, date } from 'quasar'

// Типы данных
interface PlanData {
  id: number
  mira_id: number
  planname: string
  file_id: number
  studyform: string
  studylevel: string
  vuzname: string
  faculty: string
  kafcode: number
  species: string
  napr_e: string
  napr_t: string
  lastshifr: string
  abbrprofile: string
  startyear: number
}

interface AdmissionInfo {
  [key: string]: any
}

interface CompetenceItem {
  competence_index: string
  competence: string
  type: string
}

interface DisciplineItem {
  discipline_id: number
  discipline_index: string
  discipline_name: string
  type: string[]
}

interface MatrixItem {
  type: 'group' | 'discipline'
  level: number
  discipline_id: number
  discipline_index: string
  discipline_name: string
  competence_list: Array<{
    competence_index: string
    competence: string
    type: string
    indicator_list: Array<{ indicator_index: string; indicator: string }>
  }>
}

interface SchemaItem {
  competence_index: string
  competence: string
  discipline_list: Array<{
    discipline_id: number
    discipline_index: string
    discipline_name: string
    semester_data: Array<{ semester: number; form_control: string[] }>
  }>
}

interface PassportItem {
  competence_index: string
  type: string
  competence: string
  competence_relations: string
  competence_final_indicator: string
  indicator_list: Array<{
    indicator_index: string
    indicator: string
    discipline_id: number
    discipline_index: string
    discipline_name: string
    know: string
    able: string
    own: string
    criteria: string
    methods: string
  }>
}

interface MatrixValidation {
  is_valid: boolean
  errors: Array<{
    message: string
    discipline_id?: number
    discipline_index?: string
    discipline_name?: string
    competence_index?: string
    competence?: string
  }>
  checked_at: string
  disciplines_without_competences_count?: number
  competences_without_disciplines_count?: number
}

interface SchemaValidation {
  is_valid: boolean
  errors: Array<{
    id: string
    competence_index: string
    competence_name: string
    discipline_index: string
    discipline_name: string
    discipline_id: number
    scheme_forms_count: number
    indicators_count: number
    semester: number
    message: string
  }>
  checked_at: string
  errors_count: number
}

export const useCompetencePassportStore = defineStore('competencePassport', () => {
  const currentPlanId = ref<number | null>(LocalStorage.getItem('current_plan_id') || null)
  const planData = ref<PlanData | null>(null)
  const admissionInfo = ref<AdmissionInfo | null>(null)
  const competences = ref<CompetenceItem[]>([])
  const disciplines = ref<DisciplineItem[]>([])
  const matrix = ref<MatrixItem[]>([])
  const schema = ref<SchemaItem[]>([])
  const passport = ref<PassportItem[]>([])

  const matrixValidation = ref<MatrixValidation | null>(null)
  const validating = ref(false)

  const schemaValidation = ref<SchemaValidation | null>(null)
  const validatingSchema = ref(false)
  const maxSemesters = ref(8)

  const loading = ref(false)
  const saving = ref(false)

  const currentPlanMiraId = computed(() => currentPlanId.value)

  // Валидация матрицы
  const isMatrixValid = computed(() => {
    if (!currentPlanId.value) return false

    if (matrixValidation.value?.is_valid) return true

    return localStorage.getItem(`matrix_valid_${currentPlanId.value}`) === 'true'
  })

  // Валидация схемы
  const isSchemaValid = computed(() => {
    if (!currentPlanId.value) return false
    if (schemaValidation.value?.is_valid) return true
    return localStorage.getItem(`schema_valid_${currentPlanId.value}`) === 'true'
  })

  // Валидация схемы - статус для отображения
  const schemaValidationStatus = computed(() => {
    if (validatingSchema.value) {
      return {
        type: 'info',
        title: 'Проверка ...',
        message: 'Идет проверка соответствия форм аттестации и индикаторов компетенций',
        details: false
      }
    }

    if (schemaValidation.value?.is_valid) {
      return {
        type: 'success',
        title: 'Ошибок не обнаружено!',
        message: 'Все формы аттестации соответствуют индикаторам компетенций.',
        details: true
      }
    }

    if (schemaValidation.value?.errors?.length > 0) {
      return {
        type: 'error',
        title: 'Найдены несоответствия',
        message: `Число форм аттестации не совпадает с числом индикаторов в ${schemaValidation.value.errors.length} случаях`,
        details: true
      }
    }

    return null
  })

  // Столбцы таблицы ошибок схемы
  const schemaValidationColumns = computed(() => [
    {
      name: 'competence_index',
      label: 'Код компетенции',
      field: 'competence_index',
      align: 'left',
      sortable: true
    },
    {
      name: 'discipline',
      label: 'Дисциплина',
      field: (row: any) => `${row.discipline_index} - ${row.discipline_name}`,
      align: 'left',
      sortable: true
    },
    {
      name: 'semester',
      label: 'Семестр',
      field: 'semester',
      align: 'center',
      sortable: true
    },
    {
      name: 'message',
      label: 'Ошибка',
      field: 'message',
      align: 'left',
      sortable: true
    },
    {
      name: 'actions',
      label: 'Действия',
      align: 'center'
    }
  ])

  // Форматированная дата проверки
  const lastSchemaCheckedFormatted = computed(() => {
    if (!schemaValidation.value?.checked_at) return 'еще не проверялась'
    return date.formatDate(schemaValidation.value.checked_at, 'DD.MM.YYYY HH:mm:ss')
  })

  // async function fetchCompetencePassport(planId: number) {
  //   loading.value = true
  //   try {
  //     const response = await api.get(`/api/competence-passport/${planId}/`)
  //     const data = response.data

  //     planData.value = data.plan
  //     admissionInfo.value = data.admission_info
  //     competences.value = data.competences
  //     disciplines.value = data.disciplines
  //     matrix.value = data.matrix
  //     schema.value = data.schema
  //     passport.value = data.passport

  //     currentPlanId.value = planId
  //     LocalStorage.set('current_plan_id', planId)
  //   } finally {
  //     loading.value = false
  //   }
  // }

  async function fetchPlanAdmissionData(planId: number) {
    loading.value = true
    try {
      const response = await api.get(`/api/competence-passport/${planId}/get-plan-admission/`)
      const data = response.data

      planData.value = data.plan
      admissionInfo.value = data.admission_info

      currentPlanId.value = planId
      LocalStorage.set('current_plan_id', planId)
    } finally {
      loading.value = false
    }
  }

  async function fetchReferences(planId: number) {
    loading.value = true
    try {
      const response = await api.get(`/api/competence-passport/${planId}/get-reference-data/`)
      const data = response.data

      competences.value = data.competences
      disciplines.value = data.disciplines


      currentPlanId.value = planId
      LocalStorage.set('current_plan_id', planId)
    } finally {
      loading.value = false
    }
  }

  async function fetchMatrix(planId: number) {
    loading.value = true
    try {
      const response = await api.get(`/api/competence-passport/${planId}/get-matrix-data/`)
      const data = response.data

      matrix.value = data.matrix
      
    } finally {
      loading.value = false
    }
  }

  async function fetchSchema(planId: number) {
    loading.value = true
    try {
      const response = await api.get(`/api/competence-passport/${planId}/get-schema-data/`)
      const data = response.data

      schema.value = data.schema
      let maxSemester = 8
      for (const comp of data.schema) {
        for (const disc of comp.discipline_list) {
          for (const sd of disc.semester_data) {
            if (sd.semester > maxSemester) {
              maxSemester = sd.semester
            }
          }
        }
      }
      maxSemesters.value = maxSemester
    } finally {
      loading.value = false
    }
  }

  async function fetchPassport(planId: number) {
    loading.value = true
    try {
      const response = await api.get(`/api/competence-passport/${planId}/get-passport-data/`)
      const data = response.data

      passport.value = data.passport
    } finally {
      loading.value = false
    }
  }

  // Валидация матрицы
  async function validateMatrix() {
    if (!currentPlanId.value) return

    validating.value = true
    try {
      const response = await api.get(`/api/competence-passport/${currentPlanId.value}/validate-matrix/`)
      const result: MatrixValidation = response.data

      matrixValidation.value = result

      localStorage.setItem(`matrix_valid_${currentPlanId.value}`, String(result.is_valid))

      return result
    } finally {
      validating.value = false
    }
  }

  // Обновление связей дисциплина - компетенции
  async function updateDisciplineCompetences(
    planId: number,
    disciplineId: number,
    selectedCompetences: CompetenceItem[]
  ) {
    saving.value = true
    try {
      const payload = { plan_id: planId, discipline_id: disciplineId, selected_competences: selectedCompetences }
      await api.post('/api/competence-passport/update-discipline-competences/', payload)
      //await fetchCompetencePassport(planId)
      await fetchMatrix(planId)
      await validateMatrix()
    } finally {
      saving.value = false
    }
  }

  // Валидация схемы 
  async function validateSchemeIndicators() {
    if (!currentPlanId.value) return

    validatingSchema.value = true
    try {
      const response = await api.get(`/api/competence-passport/${currentPlanId.value}/validate-scheme-indicators/`)
      const result: SchemaValidation = response.data

      schemaValidation.value = result
      localStorage.setItem(`schema_valid_${currentPlanId.value}`, String(result.is_valid))

      return result
    } finally {
      validatingSchema.value = false
    }
  }

  // Обновление схемы (формы аттестаций)
  async function updateSemesterScheme(
    planId: number,
    disciplineId: number,
    competenceIndex: string,
    competence: string,
    semester: number,
    forms: Record<string, boolean>
  ) {
    saving.value = true
    try {
      const payload = { plan_id: planId, discipline_id: disciplineId, competence_index: competenceIndex, competence, semester, forms }
      await api.post('/api/competence-passport/update-semester-scheme/', payload)
      //await fetchCompetencePassport(planId)
      //await fetchSchema(planId)
      await validateSchemeIndicators()
    } finally {
      saving.value = false
    }
  }

  // Исправление числа индикаторов по схеме
  async function fixSchemeIndicators(
    disciplineId: number,
    competenceIndex: string,
    schemeFormsCount: number,
    indicatorsCount: number
  ) {
    saving.value = true
    try {
      const payload = {
        plan_id: currentPlanId.value,
        discipline_id: disciplineId,
        competence_index: competenceIndex,
        scheme_forms_count: schemeFormsCount,
        indicators_count: indicatorsCount
      }
      
      const response = await api.post('/api/competence-passport/fix-scheme-indicators/', payload)
      const result = response.data

      //await fetchCompetencePassport(currentPlanId.value)
      await fetchSchema(currentPlanId.value)
      await validateSchemeIndicators()

      return result
    } finally {
      saving.value = false
    }
  }

  // Обновление связей компетенций
  async function updateCompetenceRelations(payload: {
    plan_id: number
    competence_index: string
    competence: string
    relations: string
  }) {
    saving.value = true
    try {
      await api.post('/api/competence-passport/update-competence-relations/', payload)
      //await fetchCompetencePassport(currentPlanId.value!)
      //await fetchPassport(currentPlanId.value!)
    } finally {
      saving.value = false
    }
  }

  // Обновление итогового индикатора
  async function updateCompetenceFinalIndicators(
    planId: number,
    competenceIndex: string,
    finalIndicatorText: string
  ) {
    saving.value = true
    try {
      const payload = { plan_id: planId, competence_index: competenceIndex, final_indicator_text: finalIndicatorText }
      await api.post('/api/competence-passport/update-competence-final-indicators/', payload)
      //await fetchCompetencePassport(currentPlanId.value!)
      //await fetchPassport(currentPlanId.value!)
    } finally {
      saving.value = false
    }
  }

  // Обновление деталей индикатора (ЗУВ, критерии, методы)
  async function updateIndicatorDetails(payload: {
    indicator_id: number
    know?: string
    able?: string
    own?: string
    criteria?: string
    methods?: string
  }) {
    saving.value = true
    try {
      await api.post('/api/competence-passport/update-indicator-details/', payload)
      //await fetchCompetencePassport(currentPlanId.value!)
      //await fetchPassport(currentPlanId.value!)
    } finally {
      saving.value = false
    }
  }

  // Создание нового индикатора
  async function createIndicator(payload: {
    //plan_id: number
    discipline_id: number
    competence_index: string
    competence: string
    indicator_index: string
    indicator: string
  }) {
    saving.value = true
    try {
      const backendPayload = {
        planlineid: payload.discipline_id,
        competence_index: payload.competence_index,
        competence: payload.competence,
        indicator_index: payload.indicator_index,
        indicator: payload.indicator
      }
        
      await api.post('/api/competence-passport/create-indicator/', backendPayload)
      //await fetchCompetencePassport(currentPlanId.value!)
      await fetchPassport(currentPlanId.value!)
    } finally {
      saving.value = false
    }
    await validateSchemeIndicators()
  }

  // Обновление существующего индикатора
  async function updateIndicator(indicatorId: number, payload: Partial<{
    discipline_id: number
    indicator_index: string
    indicator: string
  }>) {
    saving.value = true
    try {
      await api.put(`/api/competence-passport/${indicatorId}/update-indicator/`, payload)
      //await fetchCompetencePassport(currentPlanId.value!)
      await fetchPassport(currentPlanId.value!)
    } finally {
      saving.value = false
    }
  }

  // Удаление индикатора 
  async function deleteIndicator(indicatorId: number) {
    saving.value = true
    try {
      await api.delete(`/api/competence-passport/${indicatorId}/delete-indicator/`)
      //await fetchCompetencePassport(currentPlanId.value!)
      await fetchPassport(currentPlanId.value!)
      await validateSchemeIndicators()
    } finally {
      saving.value = false
    }
  }

  // Получение списка групп для выбора плана
  async function getGroupList(params: { year?: number; groupText?: string }) {
    const response = await api.get('/api/competence-passport/get-group-list/', { params })
    return response.data
  }

  async function getMatrixReport(){
    const response = await api.get(
      `/api/competence-passport/${currentPlanId.value}/get-matrix-report/`,
      { responseType: 'blob' }
    )

    let direction_code = admissionInfo.value
    let year_post = admissionInfo.value
    let filename = `${direction_code.cdirection__cod}_Матрица_компетенций_${year_post.yr}.docx`
    
    // Создаем ссылку для скачивания
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', filename)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
  }

  async function getSchemaReport(){
    const response = await api.get(
      `/api/competence-passport/${currentPlanId.value}/get-schema-report/`,
      { responseType: 'blob' }
    )

    let direction_code = admissionInfo.value
    let year_post = admissionInfo.value
    let filename = `${direction_code.cdirection__cod}_Схема_формирования_компетенций_${year_post.yr}.docx`

    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', filename)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
  }

  async function getPassportReport(){
    const response = await api.get(
      `/api/competence-passport/${currentPlanId.value}/get-passport-report/`,
      { responseType: 'blob' }
    )

    let direction_code = admissionInfo.value
    let year_post = admissionInfo.value
    let filename = `${direction_code.cdirection__cod}_Паспорт_компетенций_${year_post.yr}.docx`

    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', filename)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
  }

  // Очистка состояния 
  function clear() {
    planData.value = null
    admissionInfo.value = null
    competences.value = []
    disciplines.value = []
    matrix.value = []
    schema.value = []
    passport.value = []
    matrixValidation.value = null
    schemaValidation.value = null
    currentPlanId.value = null
    LocalStorage.remove('current_plan_id')
  }

  function hasEmptyFieldsInRelations(comp: PassportItem){
    return !comp.competence_relations?.trim()
  }

  function hasEmptyFieldsInFinalIndicator(comp: PassportItem){
    return !comp.competence_final_indicator?.trim()
  }

  function hasEmptyFieldsInIndicators(comp: PassportItem) {
    return !comp.indicator_list?.length || 
          comp.indicator_list.some((ind) => !ind.indicator?.trim())
  }

  function hasEmptyFieldsInIndicatorResult(comp: PassportItem){
    return !comp.indicator_list?.length || 
          comp.indicator_list.some((ind) => 
            !ind.know?.trim() || !ind.able?.trim() || !ind.own?.trim()
          )
  }

  function hasEmptyFieldsInAssessment(comp: PassportItem): boolean {
    return !comp.indicator_list?.length || 
          comp.indicator_list.some((ind) => 
            !ind.criteria?.trim() || !ind.methods?.trim()
          )
  }

  const competenceValidationStatus = computed(() => {
    const status: Record<string, Record<string, boolean>> = {}
    
    for (const comp of passport.value) {
      status[comp.competence_index] = {
        'competence-relations': hasEmptyFieldsInRelations(comp),
        'competence-indicators': hasEmptyFieldsInIndicators(comp),
        'final-indicator': hasEmptyFieldsInFinalIndicator(comp),
        'indicator-results': hasEmptyFieldsInIndicatorResult(comp),
        'assessment-criteria': hasEmptyFieldsInAssessment(comp)
      }
    }
    
    return status
  })

  // Ошибки в конкретной компетенции
  function hasValidationErrors(competenceIndex: string): boolean {
    const compStatus = competenceValidationStatus.value[competenceIndex]
    if (!compStatus) return false
    
    return Object.values(compStatus).some(hasError => hasError)
  }

  // Статус текущей компетенции
  const currentCompetenceValidation = computed(() => {
    return (competence: PassportItem | null) => {
      if (!competence) return {}
      
      return {
        'competence-relations': hasEmptyFieldsInRelations(competence),
        'competence-indicators': hasEmptyFieldsInIndicators(competence),
        'final-indicator': hasEmptyFieldsInFinalIndicator(competence),
        'indicator-results': hasEmptyFieldsInIndicatorResult(competence),
        'assessment-criteria': hasEmptyFieldsInAssessment(competence)
      }
    }
  })
  

  return {
    currentPlanId,
    planData,
    admissionInfo,
    competences,
    disciplines,
    matrix,
    schema,
    passport,
    matrixValidation,
    schemaValidation,
    maxSemesters,
    validating,
    validatingSchema,
    loading,
    saving,

    currentPlanMiraId,
    isMatrixValid,
    isSchemaValid,
    schemaValidationStatus,
    schemaValidationColumns,
    lastSchemaCheckedFormatted,

    competenceValidationStatus,
    hasValidationErrors,
    currentCompetenceValidation,

    //fetchCompetencePassport,
    fetchPlanAdmissionData,
    fetchReferences,
    fetchMatrix,
    fetchSchema,
    fetchPassport,
    validateMatrix,
    validateSchemeIndicators,
    fixSchemeIndicators,
    updateDisciplineCompetences,
    updateSemesterScheme,
    updateCompetenceRelations,
    updateCompetenceFinalIndicators,
    updateIndicatorDetails,
    createIndicator,
    updateIndicator,
    deleteIndicator,
    getGroupList,
    getMatrixReport,
    getSchemaReport,
    getPassportReport,
    clear
  }
})