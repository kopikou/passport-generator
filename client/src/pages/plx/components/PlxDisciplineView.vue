<script setup lang="ts">

import {storeToRefs} from "pinia";
import {api} from "boot/axios";
import {computed, ref} from "vue";
import _ from "lodash";
import {useQuasar} from "quasar";
import usePlanViewStore from "stores/planViewStore";
import SelectDialog from "components/SelectDialog.vue";

const $q = useQuasar()

const planViewStore = usePlanViewStore()
const {
  cafData,
  sync_option,
  linesData,
  disabled,
  indicatorsDataById
} = storeToRefs(planViewStore);

const filter = ref('')
const selected = ref([])

const columns = [
  {name: 'dis', field: 'dis', label: 'Дисциплина', align: 'center'},
  {name: 'newdisid', field: 'newdisid', label: 'Код', align: 'center'},
  {name: 'mustbesdudied', field: 'mustbesdudied', label: 'Изучению часов', align: 'center'},
  {name: 'hoursinzet', field: 'hoursinzet', label: 'Часов в ЗЕТ', align: 'center'},
  {name: 'caf', field: 'caf', label: 'Кафедра', align: 'center'},
  {name: 'kompetences', field: 'kompetences', label: 'Компетенции', align: 'center'},
  // {name: 'synchronize', field: 'synchronize', label: 'Синхронизировать с АИС', align: 'center'},
]

async function updateLines(values) {
  $q.loading.show()
  let r = await api.post("/api/plx/update-lines-data/", {
    data: values
  })
  $q.loading.hide()
}

const synctDataByValue = computed(() => {
  return _.keyBy(sync_option.value, 'value')
})

const cafDataById = computed(() => {
  return _.keyBy(cafData.value, 'value')
})

async function changeCaf() {
  if (selected.value.length == 0) {
    $q.notify({
      type: 'negative',
      color: 'negative',
      message: 'Вы не выбрали записи для изменения',
    })
    return
  }

  $q.dialog({
    title: 'Выберите кафедру',
    component: SelectDialog,
    componentProps: {
      options: cafData.value,
    }
  }).onOk(async (data) => {
    $q.loading.show()

    try {
      let r = await api.post("/api/plx/batch-update-caf-lines/", {
        ids: selected.value.map((x) => x.id),
        caf: data,
      })

      await planViewStore.getLinesData()

      $q.notify({
        color: 'secondary',
        message: 'Я все сделаль ^_^'
      })

    }
    catch {
      $q.notify({
        color: 'negative',
        message: 'Я не смочь, ничего не обновилось :('
      })
    }
    selected.value = []
    $q.loading.hide()
  })
}

</script>

<template>
  <div style="display: grid; grid-template-rows: auto 1fr; overflow: hidden; max-height: 100%">
    <q-table
      title="Информация о дисциплинах плана"
      :rows="linesData"
      :columns="columns"
      :rows-per-page-options="[0]"
      :filter="filter"
      row-key="id"
      wrap-cells
      hide-bottom
      selection="multiple"
      v-model:selected="selected"
      :pagination="{sortBy: 'dis'}"
    >

      <template #top-left>
        <q-btn @click="changeCaf" color="primary" label="Изменить кафедру" :disable="disabled"/>

      </template>

      <template v-slot:top-right>
        <q-input outlined dense debounce="300" v-model="filter" placeholder="Поиск" class="bg-grey-2">
          <template v-slot:append>
            <q-icon name="search"/>
          </template>
        </q-input>
      </template>

      <template v-slot:body-cell-kompetences="{row}">
        <q-td>
          <template v-for="p in _.sortBy(row.kompetences.split(','))">
            <q-chip size="md" dense v-if="p" style="cursor: pointer">
              <q-tooltip max-width="300px" style="font-size: 0.75rem;">{{ indicatorsDataById[p].indicator }}</q-tooltip>
              {{p}}
            </q-chip>

          </template>

        </q-td>
      </template>

      <template v-slot:body-cell-caf="props">
        <q-td key="caf" :props :class="props.row.caf ? 'bg-green-2' : 'bg-red-2'">
          {{ cafDataById[props.row.caf]?.label }}
          <q-popup-edit v-model="props.row.caf" v-slot="scope" @update:modelValue="updateLines(props.row)">
            <q-select
              v-model="scope.value"
              emit-value
              map-options
              :options="cafData"
              @popup-hide="scope.set"
              filled
              behavior="dialog"
              :readonly="disabled"
            >
            </q-select>
          </q-popup-edit>
        </q-td>
      </template>

<!--      <template v-slot:body-cell-synchronize="props">-->
<!--        <q-td key="synchronize" :props :class="props.row.synchronize ? 'bg-green-2' : 'bg-red-2'">-->
<!--          {{ synctDataByValue[props.row.synchronize]?.label }}-->
<!--          <q-popup-edit v-model="props.row.synchronize" v-slot="scope" @update:modelValue="updateLines(props.row)">-->
<!--            <q-select-->
<!--              v-model="scope.value"-->
<!--              emit-value-->
<!--              map-options-->
<!--              :options="sync_option"-->
<!--              @popup-hide="scope.set"-->
<!--              filled-->
<!--              :readonly="disabled"-->
<!--            >-->
<!--            </q-select>-->
<!--          </q-popup-edit>-->
<!--        </q-td>-->
<!--      </template>-->
    </q-table>
  </div>
</template>

<style scoped>

</style>
