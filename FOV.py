import pygame

tile_size = 16

class FOV:
    def __init__(self) -> None:
        pass
    ## Tile'ların durumunu değiştiren fonksiyonlar
    def set_visible(self,map, x, y):
        if 0 <= x < map.width and 0 <= y < map.height:
            map.map[y][x].visible = True

    def set_not_visible(self,map, x, y):
        if 0 <= x < map.width and 0 <= y < map.height:
            map.map[y][x].visible = False
            
    def set_explored(self,map,x,y):
         if 0 <= x < map.width and 0 <= y < map.height:
            map.map[y][x].explored = True

    def recursive_shadowcast(self, map, octant, row, start_slope, end_slope, radius, origin_x, origin_y):
        if start_slope < end_slope:
            return
        
        radius_squared = radius * radius
        for i in range(row, radius + 1):
            dx = -i - 1
            dy = -i
            blocked = False
            
            while dx <= 0:
                dx += 1
                
                # Oktant'a göre gerçek koordinatları belirle
                X, Y = self.get_coordinates(octant, dx, dy, origin_x, origin_y) # type: ignore

                # Mevcut eğim
                l_slope = (dx - 0.5) / (dy + 0.5)
                r_slope = (dx + 0.5) / (dy - 0.5)
                
                
                if start_slope < r_slope:
                    continue
                elif end_slope > l_slope:
                    break

                # Mesafe kontrolü ve görünürlük ayarı
                distance_squared = dx * dx + dy * dy
                if distance_squared < radius_squared:
                    self.set_visible(map, X, Y)
                    self.set_explored(map, X, Y)

                if blocked:
                    if map.is_blocked(X, Y):
                        new_start = r_slope
                        continue
                    else:
                        blocked = False
                        start_slope = new_start
                else:
                    if map.is_blocked(X, Y) and i < radius:
                        blocked = True
                        self.recursive_shadowcast(map, octant, i + 1, start_slope, l_slope, radius, origin_x, origin_y)
                        new_start = r_slope
            
            if blocked:
                break

    def compute_fov(self,map, player_x, player_y, radius,screen):
        # Önce tüm haritayı görünmez yap
        for y in range(map.height):
            for x in range(map.width):
                self.set_not_visible(map, x, y)

        # Ardından FOV'u hesapla ve görünür alanları belirle
        for octant in range(8):
            self.recursive_shadowcast(map, octant, 1, 1.0, 0.0, radius, player_x, player_y)
        map.map[player_y][player_x].visible = True


    def get_coordinates(self,octant, dx, dy, origin_x, origin_y):
        match octant:
            case 0:
                return origin_x + dx, origin_y + dy
            case 1:
                return origin_x + dy, origin_y + dx
            case 2:
                return origin_x + dy, origin_y - dx
            case 3:
                return origin_x + dx, origin_y - dy
            case 4:
                return origin_x - dx, origin_y - dy
            case 5:
                return origin_x - dy, origin_y - dx
            case 6:
                return origin_x - dy, origin_y + dx
            case 7:
                return origin_x - dx, origin_y + dy
    

   
