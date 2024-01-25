import ee

def GSWindicators(gsw, scale=30):
    def mapDGO(dgo):
        results = ee.Dictionary()

        results = results.combine(gsw.select('occurrence').reduceRegion(
                reducer = ee.Reducer.percentile([0,25,50,75,90,100]),
                geometry = dgo.geometry(),
                scale = scale
        ))

        results = results.combine(gsw.select('change_abs').reduceRegion(
                reducer = ee.Reducer.percentile([0,25,50,75,90,100]),
                geometry = dgo.geometry(),
                scale = scale
        ))

        results = results.combine(gsw.select('change_norm').reduceRegion(
                reducer = ee.Reducer.percentile([0,25,50,75,90,100]),
                geometry = dgo.geometry(),
                scale = scale
        ))

        results = results.combine(gsw.select('seasonality').reduceRegion(
                reducer = ee.Reducer.percentile([0,25,50,75,90,100]),
                geometry = dgo.geometry(),
                scale = scale
        ))

        results = results.combine(gsw.select('recurrence').reduceRegion(
                reducer = ee.Reducer.percentile([0,25,50,75,90,100]),
                geometry = dgo.geometry(),
                scale = scale
        ))
        
        results = results.combine(gsw.select('max_extent').reduceRegion(
                reducer = ee.Reducer.sum(),
                geometry = dgo.geometry(),
                scale = scale
        ))

        return dgo.set(results)
    return mapDGO


def calculateGSWindicators(dgos):
    gsw = ee.Image('JRC/GSW1_4/GlobalSurfaceWater')

    metrics = dgos.map(GSWindicators(gsw))

    return metrics
