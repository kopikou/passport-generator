<script setup lang="ts">

import useGeneratorViewStore from "stores/generatorViewStore";

const generatorViewStore = useGeneratorViewStore();
const mainStore = useMainStore();

const {
  cafData,
} = storeToRefs(generatorViewStore)

const {
  mira_id,
} = storeToRefs(mainStore)

import {computed, onBeforeMount, ref} from "vue";
import {api} from "boot/axios";
import {useQuasar} from "quasar";
import {GeneratorListData} from "src/types";
import {useRouter} from "vue-router";
import {storeToRefs} from "pinia";
import _ from "lodash";
import useMainStore from "stores/mainStore";
import GeneratorManageDialog from "pages/generator/components/dialogs/GeneratorManageDialog.vue";

const $q = useQuasar()
const router = useRouter()
const personListData = ref<GeneratorListData[]>([])
const adminListData = ref<GeneratorListData[]>([])

function openManageDialog(id, item) {
  $q.dialog({
    component: GeneratorManageDialog,
    componentProps: {
      id: id,
      data: item,
    }
  })
}

function filterMyList(data) {
  return _(data).orderBy(x => [x.status, x.discode], ['desc']).value()
}
function filterAllList(data) {
  return _(data).orderBy(x => [x.status, x.discode], ['desc']).value()
}

async function getProgramData() {
  let r = await api.get("/api/generator/get-program-list/")
  personListData.value = r.data.person
  adminListData.value = r.data.admin
}

const cafDataById = computed(() => {
  return _.keyBy(cafData.value, 'value')
})

function getRowColor(number) {
  return number % 2 == 0 ? 'bg-grey-3' : 'bg-white'
}

onBeforeMount(async () => {
  $q.loading.show()
  await getProgramData()
  $q.loading.hide()
})

</script>

<template>
  <div class="q-pa-lg">
    <div class="text-center text-h6 q-mb-md">Список рабочих программ дисциплин ИРНИТУ</div>
    <div>
      <div>
        <div class="text-center text-subtitle1">Ваши РПД</div>
        <q-list
          bordered
          separator
        >
          <q-expansion-item
            v-for="items, key in personListData"
            :label="key"
          >
            <q-card>
              <q-card-section>
                <div class="rpd-container">
                  <div class="rpd-row rpd-row__header text-weight-bold">
                    <div>Код</div>
                    <div>Дисциплина</div>
                    <div>Составитель</div>
                    <div>Кафедра</div>
                    <div>Статус</div>
                  </div>
                  <div class="rpd-row rpd-row__body" v-for="item, key in filterMyList(items)"
                       @click="router.push(`/generator/${item.id}/main`)">
                    <div :class="getRowColor(key)">{{ item.discode }}</div>
                    <div :class="getRowColor(key)">{{ item.discpl }}</div>
                    <div :class="getRowColor(key)">{{ item.person }}</div>
                    <div :class="getRowColor(key)">{{ cafDataById[item.kafcode]?.label }}</div>
                    <div :class="getRowColor(key)">{{ item.status_verbose }}</div>
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </q-expansion-item>
        </q-list>
      </div>
      <div>
        <div class="text-center text-subtitle1">Все РПД</div>
        <q-list
          bordered
          separator
        >
          <q-expansion-item
            v-for="items, key in adminListData"
            :label="key"
          >
            <q-card>
              <q-card-section>
                <div class="rpd-container">
                  <div class="rpd-row rpd-row__header text-weight-bold">
                    <div>Код</div>
                    <div>Дисциплина</div>
                    <div>Составитель</div>
                    <div>Кафедра</div>
                    <div>Статус</div>
                  </div>
                  <div class="rpd-row rpd-row__body" v-for="item, key in filterAllList(items)"
                       @click="openManageDialog(item.id, item)">
                    <div :class="getRowColor(key)">{{ item.discode }}</div>
                    <div :class="getRowColor(key)">{{ item.discpl }}</div>
                    <div :class="getRowColor(key)">{{ item.person }}</div>
                    <div :class="getRowColor(key)">{{ cafDataById[item.kafcode]?.label }}</div>
                    <div :class="getRowColor(key)">{{ item.status_verbose }}</div>
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </q-expansion-item>
        </q-list>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.rpd-container {
  display: grid;
  grid-template-columns: auto repeat(3, 1fr) auto;
}

.rpd-row {
  display: contents;

  $border: solid 1px silver;

  > div {
    padding: 0.5rem;
    border: $border;
    border-right: none;
    border-bottom: none;

    &:last-child {
      border-right: $border;
    }
  }

  &:last-child {
    > div {
      border-bottom: $border;
    }
  }

  &.rpd-row__body {
    &:hover {
      > div {
        background: $info !important;
        cursor: pointer;
      }
    }
  }

}

</style>
