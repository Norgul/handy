class PointSmoother:

    max_points = 5
    buffer = []
    total_x = 0
    total_y = 0

    def update(self, x, y):
        PointSmoother.buffer.append((x, y))
        PointSmoother.total_x += x
        PointSmoother.total_y += y

        if len(self.buffer) >= PointSmoother.max_points:
            old_x, old_y = PointSmoother.buffer[0]
            PointSmoother.total_x -= old_x
            PointSmoother.total_y -= old_y

            del PointSmoother.buffer[0]

    def smooth(self):
        smooth_x = PointSmoother.total_x / min(
            len(PointSmoother.buffer), PointSmoother.max_points
        )
        smooth_y = PointSmoother.total_y / min(
            len(PointSmoother.buffer), PointSmoother.max_points
        )

        return smooth_x, smooth_y
