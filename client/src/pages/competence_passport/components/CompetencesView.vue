<template>
  <layout-h-c-f>
    <template #header>
      <q-toolbar>
        <q-btn flat round dense icon="arrow_back" @click="goBack" />
        <q-toolbar-title>
          Компетенции учебного плана
        </q-toolbar-title>
        <q-btn flat label="Назад к списку" @click="goBack" />
      </q-toolbar>
    </template>

    <template #content>
      <div v-if="loading" class="text-center q-pa-lg">
        <q-spinner size="50px" color="primary" />
        <div class="q-mt-md">Загрузка компетенций...</div>
      </div>

      <div v-else-if="error" class="text-center q-pa-lg">
        <q-icon name="error" size="50px" color="negative" />
        <div class="q-mt-md text-negative">{{ error }}</div>
        <q-btn label="Попробовать снова" @click="loadCompetences" class="q-mt-md" />
      </div>

      <div v-else-if="competencesData" class="q-pa-md">
        <!-- Заголовок плана -->
        <div class="q-mb-lg">
          <h2 class="text-h4 q-mb-sm">{{ competencesData.plan_name }}</h2>
          <div class="text-subtitle1">
            <strong>Профиль:</strong> {{ competencesData.abbrprofile }} | 
            <strong>Год:</strong> {{ competencesData.startyear }}
          </div>
        </div>

        <!-- Фильтры и поиск -->
        <div class="row q-mb-md">
          <div class="col-12 col-md-6">
            <q-input
              v-model="searchText"
              placeholder="Поиск по дисциплинам и компетенциям..."
              dense
              outlined
              clearable
            >
              <template v-slot:prepend>
                <q-icon name="search" />
              </template>
            </q-input>
          </div>
          <div class="col-12 col-md-6 q-pl-md">
            <q-select
              v-model="selectedDiscipline"
              :options="disciplineOptions"
              label="Фильтр по дисциплинам"
              dense
              outlined
              clearable
              emit-value
              map-options
            />
          </div>
        </div>

        <!-- Список дисциплин с компетенциями -->
        <div v-if="filteredCompetences.length > 0">
          <q-list bordered separator>
            <q-expansion-item
              v-for="discipline in filteredCompetences"
              :key="discipline.discipline_id"
              group="disciplines"
              :label="discipline.discipline_name"
              :caption="discipline.discipline_code"
              header-class="text-weight-medium"
            >
              <!-- Дисциплина без компетенций -->
              <div v-if="discipline.competences.length === 0" class="q-pa-md text-grey">
                Нет компетенций для этой дисциплины
              </div>

              <!-- Список компетенций дисциплины -->
              <div v-else>
                <q-card flat v-for="competence in discipline.competences" :key="competence.competence_index" class="q-mb-sm">
                  <q-card-section class="q-pa-sm bg-blue-1">
                    <div class="text-weight-bold">
                      {{ competence.competence_index }}: {{ competence.competence_name }}
                    </div>
                  </q-card-section>
                  
                  <q-card-section class="q-pt-none">
                    <div v-for="indicator in competence.indicators" :key="indicator.indicator_index" class="q-pl-md q-py-xs">
                      <div class="row items-center">
                        <div class="col-auto">
                          <q-icon name="play_arrow" size="xs" color="grey" />
                        </div>
                        <div class="col">
                          <strong>{{ indicator.indicator_index }}:</strong> {{ indicator.indicator_name }}
                        </div>
                      </div>
                    </div>
                  </q-card-section>
                </q-card>
              </div>
            </q-expansion-item>
          </q-list>

          <!-- Статистика -->
          <div class="q-mt-lg text-caption text-grey">
            Найдено: {{ filteredCompetences.length }} дисциплин
          </div>
        </div>

        <div v-else class="text-center q-pa-xl">
          <q-icon name="info" size="50px" color="grey" />
          <div class="q-mt-md text-grey">Компетенции не найдены</div>
        </div>
      </div>
    </template>
  </layout-h-c-f>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCompetencePassportStore } from 'stores/competencePassportStore'
import { useQuasar } from 'quasar'
import LayoutHCF from 'components/LayoutHCF.vue'

const route = useRoute()
const router = useRouter()
const store = useCompetencePassportStore()
const $q = useQuasar()

// Реактивные данные
const loading = ref(false)
const error = ref('')
const competencesData = ref(null)
const searchText = ref('')
const selectedDiscipline = ref(null)

// Получение ID плана из URL
const planId = computed(() => route.params.planId)

// Опции для фильтра дисциплин
const disciplineOptions = computed(() => {
  if (!competencesData.value) return []
  
  return competencesData.value.competences.map(discipline => ({
    label: `${discipline.discipline_code} - ${discipline.discipline_name}`,
    value: discipline.discipline_id
  }))
})

// Фильтрация компетенций
const filteredCompetences = computed(() => {
  if (!competencesData.value) return []
  
  let filtered = competencesData.value.competences

  // Фильтр по выбранной дисциплине
  if (selectedDiscipline.value) {
    filtered = filtered.filter(discipline => 
      discipline.discipline_id === selectedDiscipline.value
    )
  }

  // Поиск по тексту
  if (searchText.value) {
    const searchLower = searchText.value.toLowerCase()
    filtered = filtered.map(discipline => {
      // Фильтруем компетенции внутри дисциплины
      const filteredCompetences = discipline.competences.filter(competence => 
        competence.competence_name.toLowerCase().includes(searchLower) ||
        competence.competence_index.toLowerCase().includes(searchLower) ||
        competence.indicators.some(indicator => 
          indicator.indicator_name.toLowerCase().includes(searchLower) ||
          indicator.indicator_index.toLowerCase().includes(searchLower)
        )
      )

      // Если есть поиск по названию дисциплины или коду
      const disciplineMatches = 
        discipline.discipline_name.toLowerCase().includes(searchLower) ||
        discipline.discipline_code.toLowerCase().includes(searchLower)

      // Возвращаем дисциплину если она сама подходит или есть подходящие компетенции
      if (disciplineMatches || filteredCompetences.length > 0) {
        return {
          ...discipline,
          competences: disciplineMatches ? discipline.competences : filteredCompetences
        }
      }
      return null
    }).filter(Boolean)
  }

  return filtered
})

// Загрузка компетенций
async function loadCompetences() {
  if (!planId.value) {
    error.value = 'ID плана не указан'
    return
  }

  loading.value = true
  error.value = ''

  try {
    competencesData.value = await store.fetchPlanCompetences(planId.value)
  } catch (err) {
    console.error('Error loading competences:', err)
    error.value = 'Ошибка при загрузке компетенций'
  } finally {
    loading.value = false
  }
}

// Навигация
function goBack() {
  router.back()
}

// Загрузка при монтировании
onMounted(() => {
  loadCompetences()
})
</script>

<style scoped lang="scss">

</style>