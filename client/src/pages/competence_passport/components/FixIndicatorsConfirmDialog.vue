<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  errorRow: any
  currentIndicators: any[] 
  competenceIndex: string
}>()

const emit = defineEmits(['ok', 'cancel'])

const actionDetails = computed(() => {
  const neededCount = props.errorRow.scheme_forms_count
  const indicators = props.currentIndicators.filter(
    ind => ind.discipline_id === props.errorRow.discipline_id
  )
  const currentCount = indicators.length

  if (neededCount > currentCount) {
    const toCreate = neededCount - currentCount
    let maxNum = 0
    
    // Находим максимальный существующий номер для создания новых индексов
    indicators.forEach(ind => {
      const regex = new RegExp(`${props.competenceIndex.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\.(\\d+)`)
      const match = ind.indicator_index.match(regex)
      if (match) maxNum = Math.max(maxNum, parseInt(match[1]))
    })

    const newIndices = []
    for (let i = 1; i <= toCreate; i++) {
      newIndices.push(`${props.competenceIndex}.${maxNum + i}`)
    }

    return {
      type: 'create',
      count: toCreate,
      items: newIndices,
      warning: 'После создания необходимо вручную заполнить содержание для новых индикаторов в паспорте.'
    }
  } else if (neededCount < currentCount) {
    const toRemove = currentCount - neededCount
    // Сортируем по убыванию индекса, чтобы удалить последние индикаторы
    const sortedInds = [...indicators].sort((a, b) => 
      b.indicator_index.localeCompare(a.indicator_index, undefined, { numeric: true })
    )
    const removeInds = sortedInds.slice(0, toRemove)

    const hasData = removeInds.some(ind => 
      ind.know || ind.able || ind.own || ind.criteria || ind.methods
    )

    return {
      type: 'delete',
      count: toRemove,
      items: removeInds.map(i => i.indicator_index),
      hasData,
      warning: hasData ? 'У некоторых удаляемых индикаторов есть заполненные данные (ЗУВ, критерии), которые будут безвозвратно потеряны!' : ''
    }
  }
  
  return null
})

function onConfirm() {
  emit('ok')
}

function onCancel() {
  emit('cancel')
}
</script>

<template>
  <q-dialog persistent >
    <q-card style="min-width: 450px">
      <q-card-section class="row items-center q-pb-none">
        <div class="text-h6">
          {{ actionDetails?.type === 'delete' ? 'Подтвердите удаление' : 'Подтвердите создание' }}
        </div>
        <q-space />
        <q-btn icon="close" flat round dense v-close-popup @click="onCancel" />
      </q-card-section>

      <q-card-section>
        <div v-if="actionDetails?.type === 'create'" class="text-body2">
          <p>Будет создано {{ actionDetails.count }} новых индикаторов:</p>
          <ul class="q-pl-md text-grey-8">
            <li v-for="idx in actionDetails.items" :key="idx">{{ idx }}</li>
          </ul>
          <q-banner rounded class="bg-warning text-white q-mt-md">
            <template v-slot:avatar>
              <q-icon name="warning" />
            </template>
            {{ actionDetails.warning }}
          </q-banner>
        </div>

        <div v-else-if="actionDetails?.type === 'delete'" class="text-body2">
          <p>Будет удалено {{ actionDetails.count }} индикатор(ов):</p>
          <ul class="q-pl-md text-grey-8">
            <li v-for="idx in actionDetails.items" :key="idx">{{ idx }}</li>
          </ul>
          
          <q-banner v-if="actionDetails.hasData" rounded class="bg-negative text-white q-mt-md">
            <template v-slot:avatar>
              <q-icon name="error" />
            </template>
            {{ actionDetails.warning }}
          </q-banner>
        </div>
      </q-card-section>

      <q-card-actions align="right">
        <q-btn flat label="Отмена" color="grey-7" v-close-popup @click="onCancel" />
        <q-btn 
          flat 
          :label="actionDetails?.type === 'delete' ? 'Удалить' : 'Создать'" 
          :color="actionDetails?.type === 'delete' ? 'negative' : 'primary'" 
          @click="onConfirm" 
          v-close-popup
        />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<style scoped lang="scss">
</style>