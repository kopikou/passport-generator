<script setup lang="ts">
import { ref, computed, onBeforeMount, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { useCompetencePassportStore } from 'src/stores/competencePassportStore'
import { storeToRefs } from 'pinia'

const route = useRoute()
const router = useRouter()
const $q = useQuasar()
const store = useCompetencePassportStore()

const {
  currentPlanId,
  competences: storeCompetences,
  loading
} = storeToRefs(store)

const searchText = ref('')
const selectedType = ref<string | null>(null)

const competenceTypes = [
  { label: 'Универсальные (УК)', value: 'Универсальная' },
  { label: 'Общепрофессиональные (ОПК)', value: 'Общепрофессиональная' },
  { label: 'Профессиональные (ПК)', value: 'Профессиональная' },
  { label: 'Дополнительные (ДК)', value: 'Дополнительная' }
]

function getTypeBadgeColor(type){
  const colors: Record<string, string> = {
    'Универсальная': 'blue',
    'Общепрофессиональная': 'green',
    'Профессиональная': 'orange',
    'Дополнительная': 'purple',
    'Другая': 'grey'
  }
  return colors[type] || 'grey'
}

function getCompetenceClass(type) {
  return `competence-${type.toLowerCase().replace(/ /g, '-')}`
}

function isTitlePageActive() {
  return route.query.section === 'title-page'
}

function isCompetenceActive(competenceIndex){
  return route.query.competence === competenceIndex && 
         route.query.section && 
         route.query.section !== 'title-page'
}

// Фильтрация
const filteredCompetences = computed(() => {
  let competences = storeCompetences.value
  
  if (searchText.value) {
    const term = searchText.value.toLowerCase().trim()
    competences = competences.filter(comp =>
      comp.competence_index.toLowerCase().includes(term) ||
      comp.competence.toLowerCase().includes(term)
    )
  }
  
  if (selectedType.value) {
    competences = competences.filter(comp =>
      comp.type === selectedType.value
    )
  }
  
  return competences
})

// Навигация
function navigateToTitlePage() {
  router.push({
    name: 'competencePassport',
    params: { id: currentPlanId.value },
    query: { section: 'title-page' }
  })
}

function navigateToCompetence(competenceIndex) {
  router.push({
    name: 'competencePassport',
    params: { id: currentPlanId.value },
    query: { 
      section: 'competence-relations',
      competence: competenceIndex 
    }
  })
}

onBeforeMount(async () => {
  if (storeCompetences.value.length === 0 && currentPlanId.value) {
    await store.fetchReferences(currentPlanId.value)
  }
})

</script>

<template>
  <div class="competence-menu" >
    <div class="menu-header q-pa-sm bg-grey-3">
      <div class="text-weight-bold">Компетенции</div>
      <div class="text-caption text-grey q-mb-sm">
        Всего: {{ filteredCompetences.length }}
      </div>
      
      <!-- Поиск и фильтры -->
      <div class="q-gutter-y-sm">
        <q-input
          v-model="searchText"
          placeholder="Поиск по индексу или содержанию..."
          dense
          outlined
          clearable
          class="bg-white"
        >
          <template v-slot:prepend>
            <q-icon name="search" />
          </template>
        </q-input>
        
        <q-select
          v-model="selectedType"
          :options="competenceTypes"
          label="Фильтр по типу"
          dense
          outlined
          clearable
          emit-value
          map-options
          class="bg-white"
        />
      </div>
    </div>

    <div v-if="loading" class="q-pa-lg text-center">
      <q-spinner color="primary" size="2em" />
      <div class="text-caption q-mt-sm">Загрузка компетенций...</div>
    </div>

    <!-- Список компетенций -->
    <div class="competence-scroll-area">
      <q-list class="competence-list q-mb-xl" dense>
        <div v-if="filteredCompetences.length === 0" class="text-center q-py-lg text-grey">
          <div v-if="searchText || selectedType">Компетенции не найдены</div>
          <div v-else>Компетенции не загружены</div>
        </div>

        <!-- Титульный лист -->
        <q-item 
          clickable
          v-ripple
          class="title-page-header"
          @click="navigateToTitlePage"
          :active="isTitlePageActive()"
          active-class="bg-amber-2 text-black"
          dense
        >
          <q-item-section>
            <q-item-label class="text-weight-medium">
              Титульный лист
            </q-item-label>
          </q-item-section>
        </q-item>

        <!-- Компетенции -->
        <q-item
          v-for="comp in filteredCompetences"
          :key="comp.competence_index"
          clickable
          v-ripple
          class="competence-header"
          :class="getCompetenceClass(comp.type)"
          @click="navigateToCompetence(comp.competence_index)"
          :active="isCompetenceActive(comp.competence_index)"
          active-class="bg-amber-2 text-black"
        >
          <q-item-section>
            <q-item-label class="text-weight-medium">
              {{ comp.competence_index }}
            </q-item-label>
          </q-item-section>
          <q-item-section side>
            <q-badge :color="getTypeBadgeColor(comp.type)" rounded>
              {{ comp.type }}
            </q-badge>
          </q-item-section>
        </q-item>
      </q-list>
    </div>
  </div>
</template>

<style scoped lang="scss">
.competence-menu {
  height: 100%;
  display: flex;
  flex-direction: column;
  
  .menu-header {
    border-bottom: 1px solid #e0e0e0;
    flex-shrink: 0;
  }
  .competence-scroll-area {
    flex: 1;
    overflow-y: auto; 
    .competence-list {
      .title-page-header {
        border-bottom: 1px solid rgba(0,0,0,0.05);
        min-height: 50px;
      }

      .competence-header {
        border-bottom: 1px solid rgba(0,0,0,0.05);
        min-height: 50px;
        
        .q-item__label {
          line-height: 1.3;
        }
      }
    }
  }
}

.q-badge {
  font-size: 10px;
  padding: 2px 6px;
  font-weight: 500;
}

:deep(.q-scrollarea__content) {
  width: 100%;
}
</style>