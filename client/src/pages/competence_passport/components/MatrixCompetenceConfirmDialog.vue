<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  addedCompetences: string[] 
  removedCompetences: string[] 
}>()

const emit = defineEmits(['ok', 'cancel'])

function onConfirm() {
  emit('ok')
}

function onCancel() {
  emit('cancel')
}
</script>

<template>
  <q-dialog persistent>
    <q-card style="min-width: 450px">
      <q-card-section class="row items-center q-pb-none">
        <div class="text-h6">Подтвердите изменение связей</div>
        <q-space />
        <q-btn icon="close" flat round dense v-close-popup @click="onCancel" />
      </q-card-section>

      <q-card-section>
        <div class="text-body2">
          <div v-if="addedCompetences.length > 0" class="q-mb-md">
            <p>Будет добавлено {{ addedCompetences.length }} компетенция(й):</p>
            <ul class="q-pl-md text-grey-8">
              <li v-for="idx in addedCompetences" :key="'add-' + idx">{{ idx }}</li>
            </ul>
            <q-banner rounded class="bg-warning text-white q-mt-sm">
              <template v-slot:avatar>
                <q-icon name="warning" />
              </template>
              Для новых компетенций будут автоматически созданы индикаторы и запись в схеме. После создания необходимо вручную заполнить содержание для новых индикаторов в паспорте.
            </q-banner>
          </div>

          <div v-if="removedCompetences.length > 0">
            <p>Будет удалено {{ removedCompetences.length }} компетенция(й):</p>
            <ul class="q-pl-md text-grey-8">
              <li v-for="idx in removedCompetences" :key="'rem-' + idx">{{ idx }}</li>
            </ul>
            <q-banner rounded class="bg-negative text-white q-mt-sm">
              <template v-slot:avatar>
                <q-icon name="error" />
              </template>
              Все индикаторы и данные схемы для этих компетенций будут безвозвратно удалены.
            </q-banner>
          </div>
        </div>
      </q-card-section>

      <q-card-actions align="right">
        <q-btn flat label="Отмена" color="grey-7" v-close-popup @click="onCancel" />
        <q-btn 
          flat 
          label="Применить изменения" 
          color="primary" 
          @click="onConfirm" 
          v-close-popup
        />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<style scoped lang="scss">
</style>