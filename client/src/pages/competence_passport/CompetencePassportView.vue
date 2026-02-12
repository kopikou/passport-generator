<script setup lang="ts">
import { ref, computed, watch, onBeforeMount, nextTick, defineAsyncComponent } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCompetencePassportStore } from 'src/stores/competencePassportStore'
import { storeToRefs } from 'pinia'
import { useQuasar } from 'quasar'

// Компоненты разделов
const TitlePageSection = defineAsyncComponent(() => import('./components/menu_sections/TitlePageSection.vue'))
const CompetenceRelationsSection = defineAsyncComponent(() => import('./components/menu_sections/CompetenceRelationsSection.vue'))
const CompetenceIndicatorsSection = defineAsyncComponent(() => import('./components/menu_sections/CompetenceIndicatorsSection.vue'))
const IndicatorDisciplinesSection = defineAsyncComponent(() => import('./components/menu_sections/IndicatorDisciplinesSection.vue'))
const IndicatorResultsSection = defineAsyncComponent(() => import('./components/menu_sections/IndicatorResultsSection.vue'))
const AssessmentCriteriaSection = defineAsyncComponent(() => import('./components/menu_sections/AssessmentCriteriaSection.vue'))

const route = useRoute()
const router = useRouter()
const $q = useQuasar()
const store = useCompetencePassportStore()

const {
  currentPlanId,
  planData,
  admissionInfo,
  passport,
  loading
} = storeToRefs(store)

const currentCompetence = ref<any>(null)

const exporting = ref(false)

async function exportPassport() {
  exporting.value = true
  try {
    store.getPassportReport()    
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: 'Ошибка при генерации документа',
      position: 'top-right'
    })
  } finally {
    exporting.value = false
  }
}

const activeTab = ref('competence-relations')
const sectionComponents = {
  'title-page': TitlePageSection,
  'competence-relations': CompetenceRelationsSection,
  'competence-indicators': CompetenceIndicatorsSection,
  'indicator-disciplines': IndicatorDisciplinesSection,
  'indicator-results': IndicatorResultsSection,
  'assessment-criteria': AssessmentCriteriaSection
}

const selectedSection = computed(() => {
  return (route.query.section as string) || ''
})

const currentCompetenceIndex = computed(() => {
  return (route.query.competence as string) || ''
})

const currentSectionComponent = computed(() => {
  if (!selectedSection.value) return null
  return sectionComponents[selectedSection.value as keyof typeof sectionComponents] || null
})

function onTabChange(tabName) {
  if (!currentCompetenceIndex.value || !currentPlanId.value || tabName === selectedSection.value) {
    return
  }
  router.push({
    name: 'competencePassport',
    params: { id: route.params.id },
    query: { 
      section: tabName,
      competence: currentCompetenceIndex.value
    }
  })
}

async function loadPlanData() {
  try {
    //await store.fetchPlanAdmissionData(currentPlanId.value)
    await store.fetchPassport(currentPlanId.value)
  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: `Ошибка загрузки данных плана: ${error.message}`,
      position: 'top-right'
    })
  }
}

async function loadCompetenceData(competenceIndex) {
  if (!competenceIndex || !currentPlanId.value) {
    currentCompetence.value = null
    return
  }
  
  try {
    const competence = passport.value.find(comp => comp.competence_index === competenceIndex)
    if (competence) {
      currentCompetence.value = competence
    } else {
      currentCompetence.value = null
      // $q.notify({
      //   type: 'warning',
      //   message: `Компетенция ${competenceIndex} не найдена в паспорте`,
      //   position: 'top-right'
      // })
    }
  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: `Ошибка загрузки данных компетенции: ${error.message}`,
      position: 'top-right'
    })
    currentCompetence.value = null
  }
}

const updateActiveTab = () => {
  if (selectedSection.value && selectedSection.value !== 'title-page') {
    activeTab.value = selectedSection.value
  }
}

onBeforeMount(async () => {
  await loadPlanData()

  if (route.query.competence) {
    await loadCompetenceData(route.query.competence as string)
  }
  
  await nextTick()
  updateActiveTab()
})

watch(
  () => route.query,
  async (newQuery) => {
    if (newQuery.section === 'title-page') {
      currentCompetence.value = null
    } else if (newQuery.competence) {
      await loadCompetenceData(newQuery.competence as string)
    } else {
      currentCompetence.value = null
    }
    await nextTick()
    updateActiveTab()
  },
  { immediate: true, deep: true }
)

watch(currentPlanId.value, async (newPlanId) => {
    if (newPlanId) {
      //await loadPlanData()
      
      if (route.query.section === 'title-page') {

      } else if (route.query.competence) {
        await loadCompetenceData(route.query.competence as string)
      }
    } else {
      currentCompetence.value = null
    }
    await nextTick()
    updateActiveTab()
  }
)
</script>

<template>
  <div class="competence-passport-view q-pa-sm">
    <div class="section-header q-mb-md">
      <div class="row justify-content-between">
        <div class="col text-h4 q-mb-xs">Паспорт компетенций</div>
          <div class="col-auto">
          <q-btn
            flat
            dense
            icon="file_download"
            label="Выгрузить"
            @click="exportPassport"
            :loading="exporting"
            class="q-mr-sm q-pr-sm bg-primary text-white"
            
          >
            <q-tooltip>Скачать паспорт компетенций в формате Word</q-tooltip>
          </q-btn>
          </div>
      </div>
      <div v-if="currentCompetence" class="text-subtitle1 text-grey">
        {{ currentCompetence.competence_index }} - {{ currentCompetence.competence }}
      </div>
      <div v-else-if="selectedSection === 'title-page'" class="text-subtitle1 text-grey">
        Титульный лист паспорта компетенций
      </div>
    </div>
    
    <div v-if="!selectedSection" class="empty-state q-pa-xl text-center">
      <span style="align-content: center; text-align: center; font-size: 20px; font-weight: bold">
        Выберите нужный раздел слева
      </span>
    </div>
    
    <div v-else class="passport-content">
      <!-- Вкладки для разделов компетенции -->
      <div v-if="selectedSection && selectedSection !== 'title-page'" class="competence-tabs q-mb-lg">
        <q-tabs
          v-model="activeTab"
          align="left"
          class="q-mb-md"
          active-bg-color="teal-1"
          @update:model-value="onTabChange"
        >
          <q-tab
            class="text-teal"
            name="competence-relations"
            label="1.1. Связь с компетенциями"
          />
          <q-tab
            class="text-teal"
            name="competence-indicators"
            label="2. Индикаторы достижения"
          />
          <q-tab
            class="text-teal"
            name="indicator-disciplines"
            label="2.1. Индикаторы и дисциплины"
          />
          <q-tab
            class="text-teal"
            name="indicator-results"
            label="2.2. Результаты обучения"
          />
          <q-tab
            class="text-teal"
            name="assessment-criteria"
            label="3. Критерии оценивания"
          />
        </q-tabs>
      </div>
      
      <!-- Динамический контент по разделам -->
      <div v-if="loading" class="text-center q-pa-lg">
        <q-spinner color="primary" size="2em" />
        <div class="text-caption q-mt-sm">Загрузка данных...</div>
      </div>
      
      <div v-else class="section-content">
        <component
          v-if="currentSectionComponent"
          :is="currentSectionComponent"
          :plan-data="planData"
          :admission-info="admissionInfo"
          :competence="currentCompetence"
          :plan-id="planData.id"
        />
        <div v-else class="text-center q-pa-xl text-grey">
          <q-icon name="error_outline" size="xl" class="q-mb-md" />
          <div class="text-h6">Раздел не найден</div>
          <div class="text-body2 q-mt-sm">Пожалуйста, выберите другой раздел</div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.competence-passport-view {
  min-height: 100%;
  
  .section-header {
    border-bottom: 1px solid #e0e0e0;
    padding-bottom: 16px;
    
    .text-subtitle1 {
      font-size: 16px;
      line-height: 1.4;
    }
  }
  
  .competence-tabs {
    .q-tabs {
      .q-tab {
        text-transform: none;
      }
    }
  }
  
  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 400px;
    
    span {
      font-size: 20px;
      font-weight: bold;
      line-height: 1.5;
    }
  }
  
  .passport-content {
    min-height: 300px;
  }
  
  .section-content {
    max-width: 1200px;
    margin: 0 auto;
  }
}
</style>